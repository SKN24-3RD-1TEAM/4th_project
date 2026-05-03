import httpx, json
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from asgiref.sync import sync_to_async
from .models import SceneModeInfo, SceneRoomSetting, SceneMessage
from apps.characters.models import CharPersona

def main_scenarios(request) :
    return render(request, 'scenarios/main.html')

# 페르소나 모델은 프로젝트 경로에 맞게 수정해주세요
# from apps.characters.models import Persona 

# =====================================================================
# 1. 시나리오 목록 및 상세 (SCR-SCENE-01)
# =====================================================================

def scene_list(request):
    """역할극 모드 전체 목록"""
    scene_list = SceneModeInfo.objects.all().order_by("title")
    context = {"scene_list": scene_list}
    return render(request, "scenarios/scene_list.html", context)

def scene_detail(request, scene_id):
    """이야기 상세 보기 모달용"""
    scene = get_object_or_404(SceneModeInfo, id=scene_id)

    chars = []
    for char in scene.chars.all():
        chars.append({
            "name": char.name,
            "role": "엑스트라" if char.is_extra else "메인 캐릭터",
            "summary": char.summary,
            "img_url": char.img_url
        })

    return JsonResponse({
        "title": scene.title,
        "summary": scene.summary,
        "keywords": [k for k in [scene.keyword1, scene.keyword2, scene.keyword3] if k],
        "characters": chars
    })

# =====================================================================
# 2. 채팅방 생성 및 진입 (SCR-SCENE-02)
# =====================================================================

@login_required(login_url="apps.auths:login")
def room_create(request, scene_id):
    """대화 시작 버튼 클릭 시 채팅방을 생성하고 방으로 이동"""
    scene = get_object_or_404(SceneModeInfo, id=scene_id)
    room = SceneRoomSetting.objects.create(
        user=request.user,
        scene=scene,
        msg_len=SceneRoomSetting.MessageLength.NORMAL
    )
    return redirect("scenarios:room_detail", room_id=room.id)

@login_required(login_url="apps.auths:login")
def room_detail(request, room_id):
    """채팅방 화면 로드"""
    room = get_object_or_404(SceneRoomSetting, id=room_id, user=request.user)
    messages = SceneMessage.objects.filter(room=room).order_by("created_at")
    
    # 페르소나가 없으면 템플릿에서 모달을 띄우도록 context로 전달
    is_persona_required = room.persona is None

    context = {
        "room": room,
        "messages": messages,
        "is_persona_required": is_persona_required,
    }
    return render(request, "scenarios/room_detail.html", context)

# =====================================================================
# 3. 페르소나 설정 및 채팅 전송 (POST 처리)
# =====================================================================

@login_required(login_url="apps.auths:login")
def setup_persona(request, room_id):
    """페르소나 모달에서 폼 제출(POST) 시 처리"""
    if request.method == "POST":
        room = get_object_or_404(SceneRoomSetting, id=room_id, user=request.user)
        scene = room.scene

        req_personality = request.POST.get("personality", "").strip()
        req_identity = request.POST.get("identity", "").strip()
        req_values = request.POST.get("values", "").strip()
        req_first_scene = request.POST.get("first_scene", "").strip()

        final_personality = req_personality if req_personality else scene.default_personality
        final_identity = req_identity if req_identity else scene.default_identity
        final_values = req_values if req_values else scene.default_values
        final_first_scene = req_first_scene if req_first_scene else scene.default_first_scene

        # 1. Persona 객체 생성 및 방에 연결 (OneToOne)
        new_persona = Persona.objects.create(
            personality=final_personality,
            identity=final_identity,
            values=final_values
        )
        room.persona = new_persona
        room.save()

        # 2. 첫 상황 설명 메시지 생성
        scene_msg = SceneMessage.objects.create(
            user=request.user,
            room=room,
            type=SceneMessage.MessageType.SITUATION,
            content=final_first_scene
        )

        return JsonResponse({
            "status": "success",
            "message": "페르소나가 저장되었습니다.",
            "first_scene_content": final_first_scene,
            "created_at": scene_msg.created_at.strftime("%Y-%m-%d %H:%M")
        })

    # POST가 아닌 잘못된 접근 시 에러 반환
    return JsonResponse({"status": "error", "message": "잘못된 요청입니다."}, status=400)

@login_required(login_url="apps.auths:login")
async def send_chat(request, room_id):
    """채팅 전송 및 답변 저장"""
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "잘못된 요청입니다."}, status=400)

    user_text = request.POST.get("content", "").strip()
    if not user_text:
        return JsonResponse({"status": "error", "message": "내용을 입력해주세요."}, status=400)

    # DB 조회 및 사용자 메시지 저장
    @sync_to_async
    def get_room_and_save_user_msg():
        room = get_object_or_404(SceneRoomSetting, id=room_id, user=request.user)
        SceneMessage.objects.create(
            user=request.user,
            room=room,
            type=SceneMessage.MessageType.USER,
            content=user_text
        )
        return room

    room = await get_room_and_save_user_msg()

    # FastAPI 호출
    @sync_to_async
    def build_payload(current_room):
        scene = current_room.scene
        recent_msgs = list(SceneMessage.objects.filter(room=current_room).order_by('-created_at')[:10])
        history = [{"type": msg.type, "content": msg.content} for msg in reversed(recent_msgs)]
        char_list = [{"name": c.name, "summary": c.summary} for c in scene.chars.all()]

        return {
            "user_message": user_text,
            "msg_len": current_room.msg_len,
            "scenario": {
                "title": scene.title,
                "summary": scene.summary,
                "characters": char_list
            },
            "history": history
        }

    payload = await build_payload(room)

    fastapi_url = ""
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(fastapi_url, json=payload)
            response.raise_for_status()
            
            ai_data = response.json()
            replies = ai_data.get("replies", [])

            # 응답받은 여러 개의 메시지를 DB에 각각 저장
            @sync_to_async
            def save_ai_replies(current_room, reply_list):
                saved_msgs = []
                scene = current_room.scene

                for reply in reply_list:
                    msg_type = reply.get("type") # "situation" 또는 "character"
                    char_name = reply.get("char_name")
                    content = reply.get("content")

                    char_obj = None
                    final_type = SceneMessage.MessageType.SITUATION
                    
                    # 캐릭터 대사인 경우
                    if msg_type == "character":
                        final_type = SceneMessage.MessageType.CHARACTER
                        if char_name:
                            char_obj = scene.chars.filter(name=char_name).first()

                    new_msg = SceneMessage.objects.create(
                        user=request.user,
                        room=current_room,
                        char=char_obj,
                        type=final_type,
                        content=content
                    )

                    saved_msgs.append({
                        "type": final_type,
                        "content": content,
                        "char_name": char_obj.name if char_obj else None,
                        "char_img_url": char_obj.img_url if char_obj else None,
                    })
                
                return saved_msgs

            new_messages = await save_ai_replies(room, replies)

            return JsonResponse({
                "status": "success",
                "new_messages": new_messages
            })

    except Exception as e:
        return JsonResponse({"status": "error", "message": "통신 중 오류가 발생했습니다."}, status=500)


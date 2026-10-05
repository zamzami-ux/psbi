from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from functools import wraps
from .models import UserProfile, Mission, Question, Choice, UserMissionProgress, UserAnswer

# =========================================
# Staff/Admin Required Decorator
# =========================================
def staff_required(view_func):
    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, 'Anda tidak memiliki akses ke halaman admin.')
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


# =========================================
# EXISTING VIEWS (unchanged)
# =========================================
@login_required(login_url='login')
def index(request):
    profile = request.user.userprofile

    # Mission stats
    all_missions = Mission.objects.all().order_by('order')
    progress_qs = UserMissionProgress.objects.filter(user=request.user)
    progress_dict = {p.mission_id: p.status for p in progress_qs}
    completed_count = progress_qs.filter(status='completed').count()
    total_missions = all_missions.count()
    path_pct = int((completed_count / total_missions * 100)) if total_missions else 0

    # XP progress to next level (500 XP per level)
    xp_in_level = profile.xp % 500
    xp_pct = int(xp_in_level / 500 * 100)

    # Learning path list
    mission_list = []
    prev_completed = True
    for m in all_missions:
        status = progress_dict.get(m.id, 'not_started')
        is_active = (status in ('reading', 'quiz', 'evaluation')) or (status == 'not_started' and prev_completed)
        mission_list.append({
            'mission': m,
            'status': status,
            'is_active': is_active,
            'is_completed': status == 'completed',
            'is_locked': status == 'not_started' and not prev_completed,
        })
        prev_completed = (status == 'completed')

    # Top leaderboard (sidebar preview — top 3 + current user)
    all_profiles = UserProfile.objects.select_related('user').order_by('-xp')[:10]
    lb_users = []
    user_rank = None
    for idx, p in enumerate(UserProfile.objects.select_related('user').order_by('-xp'), start=1):
        if p.user == request.user:
            user_rank = idx
            break
    top3 = list(UserProfile.objects.select_related('user').order_by('-xp')[:3])

    context = {
        'profile': profile,
        'xp_in_level': xp_in_level,
        'xp_pct': xp_pct,
        'xp_next': 500,
        'completed_count': completed_count,
        'total_missions': total_missions,
        'path_pct': path_pct,
        'mission_list': mission_list,
        'top3': top3,
        'user_rank': user_rank,
    }
    return render(request, 'dashboard/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Django authenticates via username. We map email to username.
        # Find user by email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
            
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Email atau Password salah!')
            
    return render(request, 'dashboard/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Validation
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar!')
            return redirect('register')
            
        # Create user (username will be the email to ensure uniqueness)
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = fullname
        user.save()
        
        messages.success(request, 'Akun berhasil dibuat! Silakan masuk.')
        return redirect('login')
        
    return render(request, 'dashboard/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def kursus(request):
    return render(request, 'dashboard/kursus.html')

@login_required(login_url='login')
def komunitas(request):
    return render(request, 'dashboard/komunitas.html')

@login_required(login_url='login')
def misi(request):
    missions = Mission.objects.all().order_by('order')
    progress_dict = {}
    for p in UserMissionProgress.objects.filter(user=request.user):
        progress_dict[p.mission_id] = p.status
    
    mission_list = []
    for mission in missions:
        mission_list.append({
            'mission': mission,
            'status': progress_dict.get(mission.id, 'not_started')
        })
    
    context = {
        'mission_list': mission_list,
    }
    return render(request, 'dashboard/misi.html', context)

@login_required(login_url='login')
def leaderboard(request):
    ranked = list(UserProfile.objects.select_related('user').order_by('-xp'))
    podium = ranked[:3]  # top 3
    rest = ranked[3:]    # rank 4+

    # Find current user rank
    user_rank = None
    for idx, p in enumerate(ranked, start=1):
        if p.user == request.user:
            user_rank = idx
            break

    context = {
        'podium': podium,
        'rest': rest,
        'user_rank': user_rank,
        'user_profile': request.user.userprofile,
    }
    return render(request, 'dashboard/leaderboard.html', context)

@login_required(login_url='login')
def pengaturan(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile
        action = request.POST.get('action', 'profile')

        if action == 'password':
            old_password = request.POST.get('old_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            if not user.check_password(old_password):
                messages.error(request, 'Password lama tidak sesuai!')
            elif new_password != confirm_password:
                messages.error(request, 'Konfirmasi password baru tidak cocok!')
            elif len(new_password) < 6:
                messages.error(request, 'Password baru minimal 6 karakter!')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # keep logged in
                messages.success(request, 'Password berhasil diubah!')
            return redirect('pengaturan')

        # --- Profile update ---
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        bio = request.POST.get('bio', '')
        is_public = request.POST.get('is_public') == 'on'
        show_in_leaderboard = request.POST.get('show_in_leaderboard') == 'on'

        user.first_name = first_name
        user.last_name = last_name
        if username and not User.objects.filter(username=username).exclude(pk=user.pk).exists():
            user.username = username
        user.save()

        profile.bio = bio
        profile.is_public = is_public
        profile.show_in_leaderboard = show_in_leaderboard
        profile.save()

        messages.success(request, 'Pengaturan berhasil disimpan!')
        return redirect('pengaturan')

    return render(request, 'dashboard/pengaturan.html')

@login_required(login_url='login')
def forgot_password(request):
    return render(request, 'dashboard/forgot-password.html')

@login_required(login_url='login')
def materi_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress, created = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
    
    if progress.status == 'not_started':
        progress.status = 'reading'
        progress.save()
        
    return render(request, 'dashboard/materi.html', {'mission': mission, 'progress': progress})

@login_required(login_url='login')
def kuis_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress, created = UserMissionProgress.objects.get_or_create(user=request.user, mission=mission)
    
    if progress.status == 'reading':
        progress.status = 'quiz'
        progress.save()
        
    questions = mission.questions.all().order_by('order')
    
    if request.method == 'POST':
        all_correct = True
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                # Save answer
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=q,
                    defaults={'choice': choice, 'is_correct': choice.is_correct}
                )
                if not choice.is_correct:
                    all_correct = False
            else:
                all_correct = False
                
        if all_correct:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
            progress.save()
            # Add XP and level up
            profile = request.user.userprofile
            profile.xp += mission.xp_reward
            profile.level = max(1, profile.xp // 500 + 1)
            profile.save()
            return redirect('misi_selesai', mission_id=mission.id)
        else:
            progress.status = 'evaluation'
            progress.save()
            return redirect('misi_evaluasi', mission_id=mission.id)
            
    return render(request, 'dashboard/kuis.html', {'mission': mission, 'questions': questions})

@login_required(login_url='login')
def evaluasi_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    progress = UserMissionProgress.objects.get(user=request.user, mission=mission)
    
    # Get questions that were answered incorrectly
    wrong_answers = UserAnswer.objects.filter(user=request.user, question__mission=mission, is_correct=False)
    questions = [wa.question for wa in wrong_answers]
    
    if request.method == 'POST':
        all_correct = True
        for q in questions:
            choice_id = request.POST.get(f'question_{q.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=q,
                    defaults={'choice': choice, 'is_correct': choice.is_correct}
                )
                if not choice.is_correct:
                    all_correct = False
            else:
                all_correct = False
                
        if all_correct:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
            progress.save()
            # Add XP and level up
            profile = request.user.userprofile
            profile.xp += mission.xp_reward
            profile.level = max(1, profile.xp // 500 + 1)
            profile.save()
            return redirect('misi_selesai', mission_id=mission.id)
        else:
            messages.error(request, 'Masih ada jawaban yang salah. Coba lagi!')
            return redirect('misi_evaluasi', mission_id=mission.id)
            
    return render(request, 'dashboard/evaluasi.html', {'mission': mission, 'questions': questions})

@login_required(login_url='login')
def selesai_view(request, mission_id):
    mission = Mission.objects.get(id=mission_id)
    return render(request, 'dashboard/selesai.html', {'mission': mission})


# =========================================
# ADMIN VIEWS
# =========================================

@staff_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_missions = Mission.objects.count()
    total_completed = UserMissionProgress.objects.filter(status='completed').count()
    avg_xp = UserProfile.objects.aggregate(avg=Avg('xp'))['avg'] or 0
    
    # Mission completion stats for bar chart
    missions = Mission.objects.all().order_by('order')
    mission_stats = []
    max_completed = 1  # avoid division by zero
    for m in missions:
        count = UserMissionProgress.objects.filter(mission=m, status='completed').count()
        if count > max_completed:
            max_completed = count
        mission_stats.append({
            'title': m.title,
            'count': count,
        })
    
    # Calculate percentage relative to max
    for ms in mission_stats:
        ms['percentage'] = int((ms['count'] / max_completed) * 100) if max_completed > 0 else 0
    
    # Recent users (last 5)
    recent_users = User.objects.select_related('userprofile').order_by('-date_joined')[:5]
    
    # Recent completions
    recent_completions = UserMissionProgress.objects.filter(
        status='completed'
    ).select_related('user', 'mission').order_by('-completed_at')[:5]
    
    context = {
        'active_page': 'dashboard',
        'total_users': total_users,
        'total_missions': total_missions,
        'total_completed': total_completed,
        'avg_xp': int(avg_xp),
        'mission_stats': mission_stats,
        'recent_users': recent_users,
        'recent_completions': recent_completions,
    }
    return render(request, 'dashboard/admin/dashboard.html', context)


@staff_required
def admin_users(request):
    users = User.objects.select_related('userprofile').all().order_by('-date_joined')
    
    # Annotate with completed missions count
    for u in users:
        u.completed_missions = UserMissionProgress.objects.filter(
            user=u, status='completed'
        ).count()
    
    context = {
        'active_page': 'users',
        'users': users,
    }
    return render(request, 'dashboard/admin/users.html', context)


@staff_required
def admin_user_edit(request, user_id):
    edit_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Update user info
        edit_user.first_name = request.POST.get('first_name', '')
        edit_user.last_name = request.POST.get('last_name', '')
        edit_user.email = request.POST.get('email', edit_user.email)
        
        username = request.POST.get('username', '')
        if username and not User.objects.filter(username=username).exclude(pk=edit_user.pk).exists():
            edit_user.username = username
        
        # Update role
        role = request.POST.get('role', 'user')
        if role == 'superuser':
            edit_user.is_staff = True
            edit_user.is_superuser = True
        elif role == 'staff':
            edit_user.is_staff = True
            edit_user.is_superuser = False
        else:
            edit_user.is_staff = False
            edit_user.is_superuser = False
        
        # Update active status
        edit_user.is_active = request.POST.get('is_active') == '1'
        edit_user.save()
        
        # Update profile
        profile = edit_user.userprofile
        profile.xp = int(request.POST.get('xp', profile.xp))
        profile.level = int(request.POST.get('level', profile.level))
        profile.bio = request.POST.get('bio', profile.bio)
        profile.save()
        
        messages.success(request, f'Data pengguna {edit_user.first_name or edit_user.username} berhasil diperbarui!')
        return redirect('admin_users')
    
    context = {
        'active_page': 'users',
        'edit_user': edit_user,
    }
    return render(request, 'dashboard/admin/user_edit.html', context)


@staff_required
def admin_user_delete(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, 'Tidak bisa menghapus superuser!')
        elif user == request.user:
            messages.error(request, 'Tidak bisa menghapus akun sendiri!')
        else:
            name = user.first_name or user.username
            user.delete()
            messages.success(request, f'Pengguna {name} berhasil dihapus.')
    return redirect('admin_users')


@staff_required
def admin_missions(request):
    missions = Mission.objects.all().order_by('order')
    
    for m in missions:
        m.question_count = m.questions.count()
        m.completed_count = UserMissionProgress.objects.filter(
            mission=m, status='completed'
        ).count()
    
    context = {
        'active_page': 'missions',
        'missions': missions,
    }
    return render(request, 'dashboard/admin/missions.html', context)


@staff_required
def admin_mission_create(request):
    if request.method == 'POST':
        mission = Mission.objects.create(
            title=request.POST.get('title', ''),
            description=request.POST.get('description', ''),
            content=request.POST.get('content', ''),
            xp_reward=int(request.POST.get('xp_reward', 50)),
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, f'Misi "{mission.title}" berhasil dibuat!')
        return redirect('admin_questions', mission_id=mission.id)
    
    context = {
        'active_page': 'missions',
        'mission': None,
    }
    return render(request, 'dashboard/admin/mission_form.html', context)


@staff_required
def admin_mission_edit(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    
    if request.method == 'POST':
        mission.title = request.POST.get('title', mission.title)
        mission.description = request.POST.get('description', mission.description)
        mission.content = request.POST.get('content', mission.content)
        mission.xp_reward = int(request.POST.get('xp_reward', mission.xp_reward))
        mission.order = int(request.POST.get('order', mission.order))
        mission.save()
        
        messages.success(request, f'Misi "{mission.title}" berhasil diperbarui!')
        return redirect('admin_missions')
    
    context = {
        'active_page': 'missions',
        'mission': mission,
        'question_count': mission.questions.count(),
    }
    return render(request, 'dashboard/admin/mission_form.html', context)


@staff_required
def admin_mission_delete(request, mission_id):
    if request.method == 'POST':
        mission = get_object_or_404(Mission, id=mission_id)
        title = mission.title
        mission.delete()
        messages.success(request, f'Misi "{title}" berhasil dihapus.')
    return redirect('admin_missions')


@staff_required
def admin_questions(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    questions = mission.questions.all().order_by('order')
    
    # Calculate next order number
    next_order = (questions.last().order + 1) if questions.exists() else 1
    
    context = {
        'active_page': 'missions',
        'mission': mission,
        'questions': questions,
        'next_order': next_order,
    }
    return render(request, 'dashboard/admin/questions.html', context)


@staff_required
def admin_question_create(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '')
        order = int(request.POST.get('order', 0))
        correct_choice = request.POST.get('correct_choice', '1')
        
        question = Question.objects.create(
            mission=mission,
            text=question_text,
            order=order,
        )
        
        # Create choices
        for i in range(1, 5):
            choice_text = request.POST.get(f'choice_{i}', '')
            if choice_text.strip():
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=(str(i) == correct_choice),
                )
        
        messages.success(request, 'Soal berhasil ditambahkan!')
    
    return redirect('admin_questions', mission_id=mission.id)


@staff_required
def admin_question_delete(request, mission_id, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id, mission_id=mission_id)
        question.delete()
        messages.success(request, 'Soal berhasil dihapus.')
    return redirect('admin_questions', mission_id=mission_id)

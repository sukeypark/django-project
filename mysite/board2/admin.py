#-*- coding:utf-8 -*-

from django.contrib import admin
from board2.models import Post, Comment
from members.models import CustomUser
from templates.commons.admin import admin_site
from datetime import datetime
from django.db.models import F
from django.conf.urls import url
from django.shortcuts import redirect


class CommentInline(admin.TabularInline):
    model = Comment
    
class AdminPost(admin.ModelAdmin):
    change_list_template = 'admin/board2/post/change_list.html'
    def delete_post(modeladmin, request, queryset):
        queryset.update(display='N')
        
    def revive_post(modeladmin, request, queryset):
        queryset.update(display='Y')
        
    def move_to_free(modeladmin, request, queryset):
        queryset.update(post_class='F')
        
    def move_to_notice(modeladmin, request, queryset):
        queryset.update(post_class='N')
        
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^auto_write/$', self.admin_site.admin_view(self.auto_write)),
        ]
        return my_urls + urls
    
    def auto_write(self, request):
        for i in range(20):
            try:
                Post.objects.filter(display='Y').update(list_order=F('list_order') + 1)
            except ValueError:
                pass
            post = Post(
                title='안녕하세요' + str(i),
                created_at = datetime.now(),
                writer = request.user.uname,
                owner = request.user,
                list_order = 1,
                display = 'Y',
                post_class = 'F',
            )
            post.save()
        return redirect('/admin/board2/post/')
           
    delete_post.short_description = "선택한 요소를 게시판에서 삭제합니다."
    revive_post.short_description = "선택한 요소를 복원합니다."
    move_to_free.short_description = "선택한 요소를 자유게시판으로 이동합니다."
    move_to_notice.short_description = "선택한 요소를 공지사항으로 이동합니다."
    
    list_display = ('title', 'writer', 'display', 'post_class')
    ordering = ('post_class', '-display', 'list_order',)
    inlines = [
        CommentInline,
    ]
    actions = [delete_post, revive_post, move_to_free, move_to_notice]
    
    fieldsets = [
        ('게시글 정보', {'fields': ['title', 'content','owner','writer']}),
        ('시간 정보', {'fields': ['created_at', 'updated_at']}),
        ('게시글 등급', {'fields': ['post_class','display']})
        
    ]
    
admin_site.register(Post, AdminPost)
admin_site.disable_action('delete_selected')
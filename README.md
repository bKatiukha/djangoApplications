 lsof -nti:8000 | xargs kill -9 
 python manage.py runserver 8000
# Django applications 
## Tasks

### Done
- [x] create simple blog with creation posts
- [x] add pagination for blog posts list
- [x] extend basic django user by custom fields
- [x] create login/registration/edit profile pages
- [x] web rtc video chat by channels
- [x] web rtc connection only logged-in users
- [x] users avatar and on video call display it
- [x] create online chat by channels
- [x] parse oryx war equipment losses by beautifulsoup4
- [x] create normal form bd tables for parsed oryx data
- [x] optimizade SQL queries for parsed oryx data

### To-Do (not a requirements just ideas)
- [ ] display all online user (not in priority)
    
- [ ] create statistic page for oryx war equipment losses with charts
- [ ] auto get oryx data parce and save in bd (maybe use celery)
    
- [ ] auto remove old chats rooms and messages (maybe use celery)   

- [ ] todo add possibility to share screen on video call
- [ ] check video call in local network if it works
- [ ] create possibilyty call with many persons (create video chat room)
- [ ] create normal visualization for video call for many persons on call
- [ ] add buttos in video call to mute and not display video
- [ ] add chat in vide call using same websocket as for p2p connection

    

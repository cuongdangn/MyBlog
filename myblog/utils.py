from myblog.models import User

def create_post_data_for_view(postdb):
    return  {
                'author': User.query.filter_by(id = postdb.user_id).first(),
                'title': postdb.title,
                'content': postdb.content,
                'date_posted': postdb.time,
                'id': postdb.id
            }

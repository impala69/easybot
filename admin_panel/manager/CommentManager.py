from easybot import models
import CustomerManager


class CommentManager:
    def __init__(self, deleted_comment_id=None):
        self.deleted_comment_id = deleted_comment_id


    def get_all_comments(self):
        result = models.Product_comment.objects.all()
        comments = []
        all_comments = []
        for comment in result:
            username_object = CustomerManager.CustomerManager(customer_id=comment.customer_id)
            comments.append(comment.pk)
            comments.append(username_object.return_username())
            comments.append(comment.product_id)
            comments.append(comment.text_comment)
            all_comments.append(comments)
            comments = []
        return all_comments

    def delete_comment(self):
        try:
            comment = models.Product_comment.objects.get(pk=self.deleted_comment_id)
            comment.delete()
            return 1
        except Exception as e:
            print e
            return 0

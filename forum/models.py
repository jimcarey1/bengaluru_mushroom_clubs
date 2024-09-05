from members.models import CustomUser
from django.db import models




class Category(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)
    y_display = models.SmallIntegerField(default=-1)
    staff_only = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-y_display"]

    def get_subcategories(self):
        return Subcategory.objects.filter(category=self)

    def __str__(self):
        return self.title + " (" + self.description + ")"


class Subcategory(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    y_display = models.SmallIntegerField(default=-1)

    class Meta:
        verbose_name_plural = "subcategories"
        ordering = ["-y_display"]

    def get_threads(self):
        return Thread.objects.all().filter(subcategory=self)

    def get_thread_count(self):
        return Thread.objects.filter(subcategory=self).count()

    def get_latest_thread(self):
        for message in Reply.objects.all().order_by("-date_posted"):
            if message.thread.subcategory == self:
                return message.thread

    def get_message_count(self):
        message_count = 0
        for thread in Thread.objects.filter(subcategory=self):
            message_count = message_count + thread.get_messages().count()
        return message_count

    def __str__(self):
        return self.title + " (" + self.description + ")"


class Thread(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    pinned = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pk"]
        permissions = [
            ("locked_thread_reply", "Can reply to a locked thread."),
            ("create_thread_in_staff_only", "Can create threads in staff only categories."),
        ]

    def get_messages(self):
        return Reply.objects.filter(thread=self).order_by('pk')

    def get_first_message(self):
        return self.get_messages().order_by('date_posted')[0]

    def get_last_message(self):
        return self.get_messages().order_by('-date_posted')[0]

    def get_participants(self):
        participants = set()
        for message in self.get_messages():
            participants.add(message.author)
        return participants

    def __str__(self):
        return self.title + " by " + self.author.username


class Reply(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField(max_length=25000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    date_edited = models.DateTimeField(null=True, blank=True)
    upvoters = models.ManyToManyField(CustomUser, blank=True, related_name='downvoters')
    downvoters = models.ManyToManyField(CustomUser, blank=True, related_name='upvoters')

    @staticmethod
    def get_recent_messages(amount):
        return Reply.objects.all().order_by('-date_posted')[:amount]

    def upvote(self, user):
        if user in self.downvoters.all():
            self.downvoters.remove(user)
        if user in self.upvoters.all():
            self.upvoters.remove(user)
        else:
            self.upvoters.add(user)
        self.save()

    def downvote(self, user):
        if user in self.upvoters.all():
            self.upvoters.remove(user)
        if user in self.downvoters.all():
            self.downvoters.remove(user)
        else:
            self.downvoters.add(user)
        self.save()

    def __str__(self):
        return self.author.username + ":" + self.content

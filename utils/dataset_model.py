import random
import time

from django.views.generic import TemplateView

from utils.config import ConfigChart, Data, Dataset


class ChartModelView(ConfigChart, TemplateView):
    template_name = 'performance.html'

    def get_context_data(self, **kwargs):
        context = super(ChartModelView, self).get_context_data(**kwargs)

        from accounts.models import CustomUser
        users = CustomUser.objects.all()

        users_info = []
        for index, user in enumerate(users, 1):
            info = {'id': user.id,
                    'name': user.get_username(),
                    'avatar': user.avatar,
                    'velocity': random.randint(1, 5)}
            users_info.append(info)

        context.update({"config": self.get_config(users_info)})
        context.update({"users": users_info})
        return context

    def get_config(self, users):
        datasets = []
        for user in users:
            dataset = Dataset(label=user['name'],
                              data=random.randint(user['id'], 1000))
            datasets.append(dataset)

        labels = []
        for i in range(7):
            date = time.strftime("%Y%m%d-%H%M%S")
            labels.append(date)
        data = Data(labels=labels, datasets=datasets)
        config = ConfigChart(data=data)

        return config.convert_to_json()

from allauth.account.adapter import DefaultAccountAdapter

class CustomUserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):

        from allauth.account.utils import user_field

        user=super().save_user(request, user, form, False)
        user_field(user, 'sexe', request.data.get('sexe', ''))
        user_field(user, 'type_personne', request.data.get('type_personne', ''))
        user_field(user, 'date_naissance', request.data.get('date_naissance', ''))
        user_field(user, 'adresse_residence', request.data.get('adresse_residence', ''))
        user_field(user, 'code_postal', request.data.get('code_postal', ''))
        user_field(user, 'ville', request.data.get('ville', ''))
        user_field(user, 'pays', request.data.get('pays', ''))
        user_field(user, 'first_name', request.data.get('first_name', ''))
        user_field(user, 'last_name', request.data.get('last_name', ''))
        user_field(user, 'num_telephone', request.data.get('num_telephone', ''))
        user.save()
        return user

        """
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = data.get('username')
        # all your custom fields
        user.sexe = data.get('sexe')
        user.num_telephone=data.get('num_telephone')
        user.date_naissance=data.get('date_naissance')
        user.adresse_residence=data.get('adresse_residence')
        user.type_personne=data.get('type_personne')
        user.code_postal=data.get('code_postal')
        user.ville=data.get('ville')
        user.pays=data.get('pays')

        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
        """
import uuid


def test_user_registration_success(web_driver_actions):
    username = str(uuid.uuid4())
    password = username
    web_driver_actions.register_user(username, password)


def test_login_success(web_driver_actions):
    username = str(uuid.uuid4())
    password = username

    web_driver_actions.register_user(username, password)
    web_driver_actions.login(username, password)


def test_logout_success(web_driver_actions):
    username = str(uuid.uuid4())
    password = username

    web_driver_actions.register_user(username, password)
    web_driver_actions.login(username, password)
    web_driver_actions.logout()


def test_create_new_note(web_driver_actions):
    username = str(uuid.uuid4())
    password = username
    note_title = username

    web_driver_actions.register_user(username, password)
    web_driver_actions.login(username, password)
    web_driver_actions.create_new_note(note_title)


def test_edit_new_note_and_logout(web_driver_actions):
    username = str(uuid.uuid4())
    password = username
    note_title = username
    after_edit_note_title = str(uuid.uuid4())

    web_driver_actions.register_user(username, password)
    web_driver_actions.login(username, password)
    web_driver_actions.create_new_note(note_title)
    web_driver_actions.edit_note(note_title, after_edit_note_title)
    web_driver_actions.logout()

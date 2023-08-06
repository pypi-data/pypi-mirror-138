from flask import url_for, request, Response
from flask_admin import expose
from flask_admin.contrib import sqla
import flask_admin as admin
from flask_admin.model import InlineFormAdmin

from twidi.admin import app, db

# Flask views
from twidi.admin.models import Device, Command, CommandTrigger, Cog, ControlMessage, NoteMessage, PointRedemption, \
    Configuration, ProgramMessage, BpmMessage, MidiMessage
from twidi.admin.views.bot import BotView
from twidi.admin.views.redemptions import RedemptionModelView
from twidi.twitch.midi_bot import TwidiBot, MidiInterface


@app.route('/')
def index():
    tmp = u"""
<p><a href="/admin/?lang=en">Manage Twidi Commands/Bots</a></p>
<p><a href="/twidi/?lang=en">Test Existing Twidi Commands</a></p>
<p><a href="/bot/?lang=en">Start/Stop Twidi Bot</a></p>
<p><a href="/bot/?lang=en">Update Username and Password</a></p>
<p><a href="/bot/?lang=en">View Logs</a></p>
"""
    return tmp


class MidiMessageModelView(sqla.ModelView):
    excluded_form_columns = ('type',)
    edit_template = 'message_edit.html'

    def __init__(self, *args, **kwargs):
        super(MidiMessageModelView, self).__init__(*args, **kwargs)
        if self.model.get_help_text:
            self.column_descriptions = self.model.get_help_text()
            return

    @expose('edit/panic_message', methods=['POST'])
    def panic(self):
        if request.method == 'POST':
            message = self.message_from_form()
            if message:
                MidiInterface().panic_device(device_id=message.device.device_id)
                return Response(status=200)

    def message_from_form(self):
        form = self.create_form()
        message = self.build_new_instance()
        form.populate_obj(message)
        return message

    @expose('edit/test_message', methods=['POST'])
    def test_midi_message(self):
        if request.method == 'POST':
            message = self.message_from_form()
            if message:
                MidiInterface().test_midi_message(message=message)
                return Response(status=200, response=message.__repr__().__str__() if message else '')
            return Response(status=200, response=message if message else '')


class NoteMessageModelView(MidiMessageModelView):
    pass


class ProgramMessageModelView(MidiMessageModelView):
    pass


class BPMMessageModelView(MidiMessageModelView):
    pass


class CommandTriggerModelView(sqla.ModelView):
    pass

# Create admin
admin = admin.Admin(app, name='Twidi Manager', template_mode='bootstrap3', base_template='layout.html', endpoint='/bot')
# Add administrative views here
admin.add_view(sqla.ModelView(Configuration, db.session, name='Configuration'))
admin.add_view(BotView(db.session, endpoint='bot', name='Bot'))
admin.add_view(sqla.ModelView(Device, db.session, name='Devices'))
admin.add_view(sqla.ModelView(Cog, db.session, name='Cogs'))
admin.add_view(sqla.ModelView(Command, db.session, name='Commands', category='Commands'))
admin.add_view(CommandTriggerModelView(CommandTrigger, db.session, name='Trigger', category='Commands'))
admin.add_view(RedemptionModelView(PointRedemption, db.session, name='Redemptions', category='Commands'))
admin.add_view(MidiMessageModelView(ControlMessage, db.session, category='Messages', name='Control Message'))
admin.add_view(NoteMessageModelView(NoteMessage, db.session, category='Messages', name='Note Message'))
admin.add_view(ProgramMessageModelView(ProgramMessage, db.session, category='Messages', name='Program Message'))
admin.add_view(BPMMessageModelView(BpmMessage, db.session, category='Messages', name='BPM Message'))

# Nested sub-menu example
# admin.add_sub_category(name="Links", parent_name="Messages")

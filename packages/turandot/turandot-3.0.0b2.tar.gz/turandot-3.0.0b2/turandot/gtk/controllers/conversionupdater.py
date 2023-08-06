from turandot.model import FrontendStrategy, CompanionData, QueueMessage, MessageType
from turandot.gtk import TurandotGtkView, guithread


class GtkConversionUpdater(FrontendStrategy):
    """GTK-specific implementation of the strategy to handle queue messages from the conversion process"""

    STATUS = {
        "idle": "IDLE",
        MessageType.EXCEPTION: "ERROR",
        MessageType.SUCCESS: "SUCCESS",
        MessageType.CANCELED: "CANCELED",
        "conv": "CONVERTING"
    }

    def __init__(self, view: TurandotGtkView):
        self.view = view
        self.warning_string: str = ""

    def handle_message(self, msg: QueueMessage):
        if msg.type == MessageType.STARTED:
            self._prime_gui(msg)
        elif msg.type == MessageType.NEXT_STEP:
            self._handle_next_step(msg)
        elif msg.type == MessageType.WARNING:
            self._handle_warning(msg)

    @guithread
    def handle_companion_data(self, data: CompanionData):
        self.view.get_element("general_status_label").set_text(
            self.STATUS[data.status.cause_of_death]
        )
        self.view.get_element("current_process_description_label").set_text("")
        if data.status.cause_of_death == MessageType.SUCCESS:
            self.view.get_element("steps_progress_bar").set_fraction(1.0)
            self.view.get_element("open_result_folder").set_visible(True)
        else:
            self.view.get_element("steps_progress_bar").set_fraction(0.0)
        if data.status.exception is not None:
            self.view.get_element("error_type_label").set_text(type(data.status.exception).__name__)
            self.view.get_element("error_text_buffer").set_text(
                "{}\n\n{}".format(str(data.status.exception), data.status.exception_tb)
            )
            self.view.get_element("error_feedback_container").set_visible(True)
        self.view.get_element("export_cancel_button").set_sensitive(False)
        self.view.get_element("export_launch_button").set_sensitive(True)

    @guithread
    def _prime_gui(self, msg: QueueMessage):
        """Reset GUI to default state at the beginning of a conversion"""
        self.view.get_element("general_status_label").set_text(self.STATUS["conv"])
        self.view.get_element("total_steps_label").set_text(str(msg.total_steps))
        self.view.get_element("n_step_label").set_text("0")
        self.view.get_element("steps_progress_bar").set_fraction(0.0)
        self.view.get_element("current_process_description_label").set_text("")
        self.view.get_element("warning_feedback_container").set_visible(False)
        self.warning_string: str = ""
        self.view.get_element("warning_text_buffer").set_text("")
        self.view.get_element("error_type_label").set_text("None")
        self.view.get_element("error_feedback_container").set_visible(False)
        self.view.get_element("error_text_buffer").set_text("")
        self.view.get_element("export_cancel_button").set_sensitive(True)
        self.view.get_element("export_launch_button").set_sensitive(False)
        self.view.get_element("open_result_folder").set_visible(False)

    @guithread
    def _handle_next_step(self, msg: QueueMessage):
        """Draw information about current conversion step to GUI"""
        self.view.get_element("n_step_label").set_text(str(msg.n_step))
        self.view.get_element("current_process_description_label").set_text(msg.step_desc)
        self.view.get_element("steps_progress_bar").set_fraction((msg.n_step -1) / msg.total_steps)

    @guithread
    def _handle_warning(self, msg: QueueMessage):
        """Draw warning message to GUI"""
        self.warning_string = "{}{}\n".format(self.warning_string, msg.warning)
        self.view.get_element("warning_text_buffer").set_text(self.warning_string)
        self.view.get_element("warning_feedback_container").set_visible(True)

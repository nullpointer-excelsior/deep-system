from persistence import create_checkpointer
from system import system_summary


def clean_current_session():
    thread_id = system_summary.cwd
    checkpoint = create_checkpointer()
    checkpoint.delete_thread(thread_id)

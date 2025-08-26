from deepsystem.persistence import create_checkpointer


def clean_session_by_thread_id(id):
    checkpoint = create_checkpointer()
    checkpoint.delete_thread(id)
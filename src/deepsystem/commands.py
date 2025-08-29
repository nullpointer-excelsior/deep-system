import click
from deepsystem.question import invoke as invoke_question
from deepsystem.config import update_ai_model, get_configuration
from deepsystem.system import system_summary
from deepsystem import sessions
from deepsystem.history import find_messages_by_thread_id, get_code_snippets_by_thread_id
from deepsystem import ui
import pyperclip 
from rich.console import Console


console = Console()
configuration = get_configuration()


def session_option():
    def decorator(wrapper_fn):
        return click.option("-s", "--session", "session", help="Set a session name for the conversation.")(wrapper_fn)
    return decorator


@click.command(help='Make a question with session based on the current working directory')
@click.argument('question', required=False)
@click.option("-f", "--file", "selectfile", count=True, help="Select a file with fzf to ask a question about this file. you can pass a multiple files using the short option repeatedly eg: '-sss' select 3 files") # TODO: Using the count option might enable selecting multiple files
@click.option("-c", "--from-clipboard", "fromclipboard", is_flag=True, help="Add clipboard content to question.")
@session_option()
def question(question, selectfile, fromclipboard, session):
    
    contextfiles = []

    for _ in range(selectfile):
        if fileselected := ui.select_files():
            contextfiles.append(fileselected)

    if contextfiles:
        console.print("\n[bold]📝 Context files added:[/]")
        console.print("\n".join(f"[grey42]- {f}[/]" for f in contextfiles))

    clipboard_content = pyperclip.paste() if fromclipboard else None

    if not question:
        question = click.prompt(click.style("\n💬 Enter your question", fg="yellow"), type=str)

    model = configuration['ai']['model']['selected']    

    with console.status(f"[bold green] 🦜 Thinking and hallucinating with {model}...[/]", spinner="dots"):
        response = invoke_question(question, contextfiles=contextfiles, clipboard=clipboard_content, session=session)
    
    ui.display_markdown(response["answer"])

                                                                                                                                                                                                                                                                            
@click.group()                                                                                                                                                                                                                                                              
def history():                                                                                                                                                                                                                                                              
    """History related commands"""                                                                                                                                                                                                                                          
    pass                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                            
@history.command(help="Show message history")   
@session_option()                                                                                                                                                                                                                                                       
def messages(session):                                                                                                                                                                                                                                                             
    message_icons = {
        "ai": "🤖 AI:",
        "human": "🐵 User:"
    }
    thread_id = session if session else system_summary.cwd
    for message in find_messages_by_thread_id(thread_id):
        if message.type == "human":
            console.print(f"\n{message_icons.get('human')} [bold green]{message.content}[/bold green]\n")   
            continue
        console.print(message_icons.get(message.type, "👤 Unknown:"))
        ui.display_markdown(message.content)



@history.command(help="Show code snippets from history")  
@session_option()                                                                                                                                                                                                                                                        
def code(session):    
    thread_id = session if session else system_summary.cwd
    snippets = get_code_snippets_by_thread_id(thread_id)
    if not snippets:
        console.print("🚫 Snippets not found")
        return

    if code := ui.select_code_snippet(snippets):
        ui.display_code(code)                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                            

@click.command(help='Clean chat session')
@session_option()
def clean(session):
    thread_id = session if session else system_summary.cwd
    sessions.clean_session_by_thread_id(thread_id)  
    console.print("🧹 [bold green]Session cleaned [/bold green]")


@click.command(help='Update model based on configured choices')
def model():
    
    config = get_configuration()
    modeloptions = config["ai"]["model"]["choices"]
    
    if selected := ui.select_options(modeloptions):
        update_ai_model(selected)
        console.print("🚀 [bold green]Model updated [/bold green]") 

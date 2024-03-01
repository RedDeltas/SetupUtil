import click
from setup_scripts.banner import banner
from setup_scripts.questionary_option import QuestionaryOption
from setup_scripts.load_models_from_huggingface import load_models_from_huggingface


activity_funcs = {
    "Load models from HuggingFace": load_models_from_huggingface
}

@click.command()
@click.option('--activity', prompt='What would you like to do?', type=click.Choice(activity_funcs.keys(), case_sensitive=False), cls=QuestionaryOption)
def cli(**kwargs):
    activity_func = activity_funcs.get(kwargs["activity"])
    activity_func()

def banner_wrapper():
    print(banner)
    cli()

if __name__ == '__main__':
    print(banner)
    cli()
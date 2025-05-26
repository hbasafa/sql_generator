
from omegaconf import OmegaConf
from langchain_core.prompts import ChatPromptTemplate
from src.app import settings
from src.logging.log_manager import logger
from src.utils.search import find_all_matches


class Prompting:
    templates = None

    TEMPLATE_GREETING = "greeting"
    TEMPLATE_SQL_GENERATION = "sql_generation"
    TEMPLATE_SQL_PAIRS = "sql_pairs"
    TEMPLATE_DATA_SAMPLES = "data_samples"

    @classmethod
    def load_templates(cls):
        if cls.templates is None:
            logger.info("Loading prompt templates...")
            cls.templates = OmegaConf.load(settings.LLM_TEMPLATES_PATH).prompt_templates
        return cls.templates

    @classmethod
    def get_user_template(cls, template_name):
        return cls._get_nodes(template_name)[0].user_template

    @classmethod
    def get_system_template(cls, template_name):
        return cls._get_nodes(template_name)[0].system_template

    @classmethod
    def create_prompt(cls, template, **kwargs):
        prompt = ChatPromptTemplate.from_template(template)
        return prompt.invoke(kwargs)

    @classmethod
    def create_messages(cls, template_name, **kwargs):
        user_prompt = cls.get_user_template(template_name)
        system_prompt = cls.get_system_template(template_name)
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_prompt), ("user", user_prompt)]
        )
        return prompt_template.invoke(kwargs).to_messages()

    @classmethod
    def _get_nodes(cls, name):
        return find_all_matches(cls.templates, {"name": name})
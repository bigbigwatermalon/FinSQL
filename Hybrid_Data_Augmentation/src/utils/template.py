import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from .extra import get_logger

logger = get_logger(__name__)


@dataclass
class Format:
    prompt: str


templates: Dict[str, Format] = {}


@dataclass
class Template:
    name: str

    def __post_init__(self):
        """
        Method to initialize Template objects after __init__.

        This method checks if the name of the Template object exists in the templates dictionary.
        If it exists, it assigns the corresponding prompt value from the templates dictionary to the Template object's prompt attribute.
        If it does not exist, it raises a ValueError with a message stating that the template does not exist.

        :return: None
        :raises ValueError: If the template with the given name does not exist.
        """
        if self.name in templates:
            self.prompt = templates[self.name].prompt
        else:
            raise ValueError("Template {} does not exist.".format(self.name))

    def get_prompt(self, variables: Dict[str, str]) -> str:
        """
        :param variables: A dictionary containing variable names and their corresponding values.
        :return: A string representing the formatted prompt.
        """
        if len(variables) == 0:
            return ""
        return self._format_example(variables)

    def _format_example(self, variables: Dict[str, str]) -> str:
        """
        Format an example string by replacing variables with values.

        :param variables: A dictionary mapping variable names to their corresponding values.
        :type variables: Dict[str, str]
        :return: The formatted example string.
        :rtype: str
        """
        formatted_string = self.prompt.format_map(variables)
        return formatted_string



def register_template(name: str, prompt: str) -> None:
    templates[name] = Format(
        prompt=prompt,
    )


with open("configures/templates.json", "r") as f:
    template_map = json.load(f)

for template_name, prompt_template in template_map.items():
    register_template(
        name=template_name,
        prompt=prompt_template
    )

logger.info(f"Register Templates Successfully")



if __name__ == "__main__":
    template = Template("instruction_cot_spider_1")
    variables = {
        "schema": "[This is schema]",
        "fks": "[This is fks]",
        "question": "[This is question]"
    }
    print(template.get_prompt(variables))
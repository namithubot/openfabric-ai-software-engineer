import os
import warnings
from typing import Dict

from openfabric_pysdk.utility import SchemaUtil

from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from openfabric_pysdk.context import Ray, State
from openfabric_pysdk.loader import ConfigClass
from chat import get_bot_response


############################################################
# Callback function called on update config
############################################################
def config(configuration: Dict[str, ConfigClass], state: State):
    # TODO Add code here
    pass


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: Ray, state: State) -> SimpleText:
    output = []
    context = [{"role": "system", "content": "You are a tutor for a student who explains everything with the simplest explanation"}]
    for text in request.text:
        # TODO Add code here
        conext.append({ "role": "user",  "content": text})
        response = get_bot_response(conext)
        contex.append({"role": "assistant", "content": resp})
        output.append(response)

    return SchemaUtil.create(SimpleText(), dict(text=output))

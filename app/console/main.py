from google import genai
from google.genai import types
from datetime import datetime
import logging
import func_mod
from ..core.config import AI_TOKEN

logger = logging.getLogger(__name__)


def handle_function_call_response(
    model: str,
    config: types.GenerateContentConfig,
    client: genai.Client,
    func_module,
    response: types.GenerateContentResponse,
    contents: list[types.Content]
) -> tuple[str, list[types.Content]]:
    '''Process a response for function calls, execute the function, and recurse if needed.'''
    logger.debug("Starting handle_function_call_response")
    # Iterate over parts of the model's first candidate
    for part in response.candidates[0].content.parts:
        logger.debug(f"Processing part: {part}")
        if part.function_call:
            tool_call = part.function_call
            logger.debug(f"Found function call: {tool_call.name} with args: {tool_call.args}")

            # Find and invoke the function
            func = getattr(func_module, tool_call.name, None)
            if not callable(func):
                result = "Функция недоступна (not callable)"
                logger.warning(f"Requested function '{tool_call.name}' is not callable or not found.")
            else:
                try:
                    logger.debug(f"Calling function '{tool_call.name}' with arguments: {tool_call.args}")
                    result = func(**tool_call.args)
                    logger.info(f"Function '{tool_call.name}' executed successfully: {result}")
                except Exception as e:
                    result = f"Произошла ошибка: {e}"
                    logger.error(f"Error during function execution '{tool_call.name}': {e}", exc_info=True)

            # Append the function call and its result as new contents
            contents.append(
                types.Content(role="assistant", parts=[types.Part(function_call=tool_call)])
            )
            contents.append(
                types.Content(
                    role="assistant",
                    parts=[types.Part.from_function_response(name=tool_call.name, response={"result": result})]
                )
            )

            # Generate a new model response after executing the tool
            try:
                logger.debug("Generating follow-up content after function call.")
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config
                )
                logger.info("Received follow-up model response.")
            except Exception as e:
                logger.error(f"Error during content generation: {e}", exc_info=True)

            # After handling one function call, break to re-scan updated response
            break

    # Check if the new response contains another function call
    for part in response.candidates[0].content.parts:
        if part.function_call:
            logger.debug("Detected nested function call, recursing...")
            return handle_function_call_response(model, config, client, func_module, response, contents)

    logger.debug("Completed handle_function_call_response")
    # Return final assistant text and full conversation
    return response.text or "", contents


def generate_response_function_call(
    client: genai.Client,
    config: types.GenerateContentConfig,
    model: str,
    func_module,
    request: str,
    contents: list[types.Content]
) -> tuple[str, list[types.Content]]:
    '''Initial wrapper: send user request, then process function calls.'''
    logger.debug(f"Request text: {request}")
    contents.append(types.Content(role="user", parts=[types.Part(text=request)]))

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=config
        )
        logger.info("Initial model response received.")
    except Exception as e:
        logger.error(f"Error during initial content generation: {e}", exc_info=True)
        return "Бип-боп, произошла ошибка :C\nПопробуйте ещё раз!", contents

    return handle_function_call_response(model, config, client, func_module, response, contents)


# Define the tools
new_reminder_function = {
    "name": "new_reminder",
    "description": "sets the reminder. Datetime must be formatted 'DD.MM.YYYY HH:MM'",
    "parameters": {
        "type": "object",
        "properties": {
            "datetime_str": {"type": "string"},
            "title": {"type": "string"},
            "description": {"type": "string"}
        },
        "required": ["title", "datetime_str"]
    }
}

tools = types.Tool(function_declarations=[new_reminder_function])


# Main loop
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    client = genai.Client(api_key=AI_TOKEN)
    contents: list[types.Content] = []

    while True:
        user_input = input("You: ")
        with open("system_instruction.txt", "r", encoding="utf-8") as f:
            system_instruction = f.read().strip()

        # Add current timestamp to system instruction
        timestamp = datetime.now().strftime('%d.%m.%Y, %H:%M')
        config = types.GenerateContentConfig(
            tools=[tools],
            system_instruction=f"{system_instruction}\nСейчас {timestamp}",
            temperature=0.3
        )

        bot_response, contents = generate_response_function_call(
            client,
            config,
            model="gemini-2.0-flash-lite",
            func_module=func_mod,
            request=user_input,
            contents=contents
        )
        print("Bot:", str(bot_response).rstrip(".\n"))

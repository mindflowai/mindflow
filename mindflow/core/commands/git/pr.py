import asyncio
from typing import List, Optional, Tuple

from result import Err, Ok, Result

from mindflow.core.settings import Settings
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import PR_BODY_PREFIX
from mindflow.core.prompts import PR_TITLE_PREFIX
from mindflow.core.types.model import ConfiguredTextCompletionModel, ModelApiCallError


async def create_gpt_title_and_body(
    settings: Settings, diff_output: str, title: Optional[str], body: Optional[str]
) -> Result[Tuple[str, str], ModelApiCallError]:
    query_model: ConfiguredTextCompletionModel = settings.mindflow_models.query.model

    tasks: List[asyncio.Task[Result[str, ModelApiCallError]]] = []
    if title is None:
        tasks.append(
            asyncio.create_task(
                query_model.call_api(
                    build_prompt_from_conversation_messages(
                        [
                            create_conversation_message(
                                Role.SYSTEM.value, PR_TITLE_PREFIX
                            ),
                            create_conversation_message(Role.USER.value, diff_output),
                        ],
                        query_model,
                    )
                )
            )
        )
    if body is None:
        tasks.append(
            asyncio.create_task(
                query_model.call_api(
                    build_prompt_from_conversation_messages(
                        [
                            create_conversation_message(
                                Role.SYSTEM.value, PR_BODY_PREFIX
                            ),
                            create_conversation_message(Role.USER.value, diff_output),
                        ],
                        query_model,
                    )
                )
            )
        )

    results: List[Result[str, ModelApiCallError]] = await asyncio.gather(*tasks)

    title_response = results[0] if title is None else Ok(title)
    body_response = results[1] if body is None else Ok(body)

    if isinstance(title_response, Err):
        return title_response
    if isinstance(body_response, Err):
        return body_response

    return Ok((title_response.value, body_response.value))

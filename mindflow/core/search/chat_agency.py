from typing import List

from mindflow.core.convo import Conversation, estimate_tokens, get_chat_model


def run_agent_query(document_paths: List[str], user_query: str):
    # if the document paths contains only files that are reasonably small, then we don't need to run any kind of
    # search, we can just concatenate the files and return the result.

    convo = Conversation(conversation_id=0)

    tokens, texts = estimate_tokens(document_paths, user_query, return_texts=True)

    chat_model = get_chat_model()
    if tokens > chat_model.hard_token_limit:
        raise NotImplementedError(
            f"{tokens} is too large (for now), max is {chat_model.hard_token_limit}."
        )

    user_query = "\n".join(texts)
    convo.add_message(user_query)
    response = convo.get_response()

    if response is None:
        return "Unable to generate response. Please try again and if the problem persists, please raise an issue at: https://github.com/nollied/mindflow/issues."

    # track the response
    convo.add_message(response, role="assistant")

    convo.save()
    return response

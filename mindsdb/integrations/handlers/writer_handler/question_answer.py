from collections import defaultdict
from datetime import datetime

import pandas as pd
from langchain.chains import RetrievalQA
from langchain.llms import Writer

from mindsdb.utilities.log import get_log
from .settings import ModelParameters
from .settings import get_retriever

logger = get_log(logger_name=__name__)


class QuestionAnswerer:

    def __init__(self, args: dict, model_parameters: ModelParameters):
        self.output_data = defaultdict(list)

        llm = Writer(
            **model_parameters.dict()
        )
        retriever = get_retriever(embeddings_model_name)
        self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                              return_source_documents=True, callbacks=model_parameters.callbacks)

    @property
    def results_df(self):
        return pd.DataFrame(self.output_data)

    def query(self, input_query: str):
        logger.debug(f"Querying: {input_query}")

        res = self.qa(input_query)

        self.output_data["question"].append(input_query)
        self.output_data["answer"].append(res['result'])

        sources = defaultdict(list)

        for idx, document in enumerate(res['source_documents']):
            sources['sources_document'].append(document.metadata["source"])
            sources['sources_row'].append(document.metadata.get("row", None))
            sources['sources_content'].append(document.page_content)

        self.output_data["source_documents"].append(dict(sources))

    def output(self, output_path: str):
        # output results
        date_time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.results_df.to_csv(output_path / f"answers-{date_time_now}-output.csv", index=False)
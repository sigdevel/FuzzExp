





"""
FILE: sample_analyze_healthcare_entities_async.py

DESCRIPTION:
    This sample demonstrates how to detect healthcare entities in a batch of documents.

    In this sample we will be a newly-hired engineer working in a pharmacy. We are going to
    comb through all of the prescriptions our pharmacy has fulfilled so we can catalog how
    much inventory we have.

USAGE:
    python sample_analyze_healthcare_entities_async.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_LANGUAGE_ENDPOINT - the endpoint to your Language resource.
    2) AZURE_LANGUAGE_KEY - your Language subscription key
"""

from __future__ import annotations
import asyncio


async def sample_analyze_healthcare_entities_async() -> None:

    print(
        "In this sample we will be combing through the prescriptions our pharmacy has fulfilled "
        "so we can catalog how much inventory we have"
    )
    print(
        "We start out with a list of prescription documents."
    )

    
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import HealthcareEntityRelation
    from azure.ai.textanalytics.aio import TextAnalyticsClient

    endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
    key = os.environ["AZURE_LANGUAGE_KEY"]

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    documents = [
        """
        Patient needs to take 100 mg of ibuprofen, and 3 mg of potassium. Also needs to take
        10 mg of Zocor.
        """,
        """
        Patient needs to take 50 mg of ibuprofen, and 2 mg of Coumadin.
        """
    ]

    async with text_analytics_client:
        poller = await text_analytics_client.begin_analyze_healthcare_entities(documents)
        result = await poller.result()
        docs = [doc async for doc in result if not doc.is_error]

    print("Let's first visualize the outputted healthcare result:")
    for doc in docs:
        for entity in doc.entities:
            print(f"Entity: {entity.text}")
            print(f"...Normalized Text: {entity.normalized_text}")
            print(f"...Category: {entity.category}")
            print(f"...Subcategory: {entity.subcategory}")
            print(f"...Offset: {entity.offset}")
            print(f"...Confidence score: {entity.confidence_score}")
            if entity.data_sources is not None:
                print("...Data Sources:")
                for data_source in entity.data_sources:
                    print(f"......Entity ID: {data_source.entity_id}")
                    print(f"......Name: {data_source.name}")
            if entity.assertion is not None:
                print("...Assertion:")
                print(f"......Conditionality: {entity.assertion.conditionality}")
                print(f"......Certainty: {entity.assertion.certainty}")
                print(f"......Association: {entity.assertion.association}")
        for relation in doc.entity_relations:
            print(f"Relation of type: {relation.relation_type} has the following roles")
            for role in relation.roles:
                print(f"...Role '{role.name}' with entity '{role.entity.text}'")
        print("------------------------------------------")

    print("Now, let's get all of medication dosage relations from the documents")
    dosage_of_medication_relations = [
        entity_relation
        for doc in docs
        for entity_relation in doc.entity_relations if entity_relation.relation_type == HealthcareEntityRelation.DOSAGE_OF_MEDICATION
    ]
    

    print(
        "Now, I will create a dictionary of medication to total dosage. "
        "I will use a regex to extract the dosage amount. For simplicity sake, I will assume "
        "all dosages are represented with numbers and have mg unit."
    )
    import re
    from collections import defaultdict

    medication_to_dosage: dict[str, int] = defaultdict(int)

    for relation in dosage_of_medication_relations:
        

        dosage_role = next(filter(lambda x: x.name == "Dosage", relation.roles))
        medication_role = next(filter(lambda x: x.name == "Medication", relation.roles))

        try:
            dosage_value = int(re.findall(r"\d+", dosage_role.entity.text)[0]) 
            medication_to_dosage[medication_role.entity.text] += dosage_value
        except StopIteration:
            
            pass

    [
        print("We have fulfilled '{}' total mg of '{}'".format(
            dosage, medication
        ))
        for medication, dosage in medication_to_dosage.items()
    ]


async def main():
    await sample_analyze_healthcare_entities_async()


if __name__ == '__main__':
    asyncio.run(main())

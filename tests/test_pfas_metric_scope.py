from scripts.audit_pfas_retrieval_metric_scope import scope_selection


def test_scope_is_selected_by_question_permission_not_system_or_score():
    gold = {"qa_questions": [
        {"question_id": "permitted", "question": "Compare parent-removal/degradation outcomes.",
         "required_key_points": ["Reported parent removal and separate defluorination.", "Do not rank catalysts."]},
        {"question_id": "not_permitted", "question": "Was the PFAS chemically degraded?",
         "required_key_points": ["Removal alone is insufficient."]}]}
    assert scope_selection(gold) == {"permitted": [0]}

from feedback import CloudNexus, Feedback, Plan

def test_provide_feedback():
    cloud_nexus = CloudNexus()
    plan_id = 1
    rating = 5
    comment = "Great plan!"
    cloud_nexus.provide_feedback(plan_id, rating, comment)
    feedback = cloud_nexus.get_feedback(plan_id)
    assert len(feedback) == 1
    assert feedback[0].plan_id == plan_id
    assert feedback[0].rating == rating
    assert feedback[0].comment == comment

def test_get_feedback():
    cloud_nexus = CloudNexus()
    plan_id = 1
    rating = 5
    comment = "Great plan!"
    cloud_nexus.provide_feedback(plan_id, rating, comment)
    feedback = cloud_nexus.get_feedback(plan_id)
    assert len(feedback) == 1
    assert feedback[0].plan_id == plan_id
    assert feedback[0].rating == rating
    assert feedback[0].comment == comment

def test_is_nlp_model_trained():
    cloud_nexus = CloudNexus()
    plan_id = 1
    rating = 5
    comment = "Great plan!"
    cloud_nexus.provide_feedback(plan_id, rating, comment)
    assert cloud_nexus.is_nlp_model_trained()

def test_empty_feedback():
    cloud_nexus = CloudNexus()
    plan_id = 1
    feedback = cloud_nexus.get_feedback(plan_id)
    assert len(feedback) == 0

def test_untrained_nlp_model():
    cloud_nexus = CloudNexus()
    assert not cloud_nexus.is_nlp_model_trained()

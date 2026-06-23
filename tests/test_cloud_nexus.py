from cloud_nexus import CloudNexus

def test_validate_plan_pass():
    nexus = CloudNexus()
    project_name = "Test Project"
    plan = "This is a microservices architecture"
    assert nexus.validate_plan(project_name, plan) == True
    assert nexus.get_validation_results(project_name) == ["Pass", "Pattern Microservices found"]

def test_validate_plan_fail():
    nexus = CloudNexus()
    project_name = "Test Project"
    plan = "This is a custom architecture"
    assert nexus.validate_plan(project_name, plan) == False
    assert nexus.get_validation_results(project_name) == ["Fail", "No pattern found"]

def test_get_validation_results():
    nexus = CloudNexus()
    project_name = "Test Project"
    plan = "This is a microservices architecture"
    nexus.validate_plan(project_name, plan)
    assert nexus.get_validation_results(project_name) == ["Pass", "Pattern Microservices found"]

def test_get_validation_results_non_existent_project():
    nexus = CloudNexus()
    project_name = "Non Existent Project"
    assert nexus.get_validation_results(project_name) == None

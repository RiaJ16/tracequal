def update(project_id):
    from api.models import Code, Link, Progress, Requirement, Test, UserStory
    user_stories = UserStory.objects.filter(project_id=project_id,
                                            archived=False)
    requirements = Requirement.objects.filter(project_id=project_id,
                                              archived=False)
    code_artifacts = Code.objects.filter(project_id=project_id,
                                         archived=False)
    total_linked = 0
    for user_story in user_stories:
        if Link.objects.filter(from_art=user_story.id, archived="False",
            from_art__archived=False, to_art__archived=False).exists():
            total_linked += 1
    if user_stories:
        req_progress = total_linked / len(user_stories) * 100
    else:
        req_progress = 0
    total_linked_design = 0
    total_linked_code = 0
    for requirement in requirements:
        if Link.objects.filter(from_art=requirement.id, to_art__type="design",
        archived=False, from_art__archived=False, to_art__archived=False).exists():
            total_linked_design += 1
        if Link.objects.filter(from_art=requirement.id, to_art__type="code",
        archived=False, from_art__archived=False, to_art__archived=False).exists():
            total_linked_code += 1
    if requirements:
        design_progress = total_linked_design / len(requirements) * 100
        code_progress = total_linked_code / len(requirements) * 100
    else:
        design_progress = 0
        code_progress = 0
    total_linked = 0
    for code in code_artifacts:
        links = Link.objects.filter(from_art=code.id, to_art__type="test",
        archived=False, from_art__archived=False, to_art__archived=False)
        for link in links:
            try:
                linked_test = Test.objects.get(id=link.to_art.id, archived=False)
                if linked_test.verdict == "pass":
                    total_linked += 1
                    break
            except Test.DoesNotExist:
                pass
    if code_artifacts:
        test_progress = total_linked / len(code_artifacts) * 100
    else:
        test_progress = 0
    progress_ = Progress.objects.get(project_id=project_id)
    progress_.progress_requirements = req_progress
    progress_.progress_design = design_progress
    progress_.progress_code = code_progress
    progress_.progress_tests = test_progress
    progress_.save()

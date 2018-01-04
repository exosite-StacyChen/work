
Murano CLI can syncup all project
    [Setup]    TestSetupForCreateFileAndSolution
    [Template]    Syncup All Porject And Verify Porject Is Synced
    syncup
    push
    [Teardown]    TestTeardownForDeleteAllDirectory

Syncup All Porject And Verify Porject Is Synced
    [Arguments]    ${command}
    Create All Service File
    ${resp} =    Shell Call    murano    ${command}
    Verify Two Specific Parameters From Gateway Info Should Contain Expected    ${applicationID}    resources    ${random}    ${resourceContent}

    get module list    solutionId
    solution_solutionID_endpoint_get    solutionID
    get_serviceconfig_via_api    solutionID

TestTeardownForDeleteAllDirectory
    Remove Directory    ${modulesDir}    recursive=True
    Remove Directory    ${resourceDir}    recursive=True
    Remove Directory    ${routesDir}    recursive=True
    Remove Directory    ${servicesDir}    recursive=True

TestSetupForCreateFileAndSolution
    Set Test Variable    ${modulesDir}    ${CURDIR}/modules
    Set Test Variable    ${routesDir}    ${CURDIR}/routes
    Set Test Variable    ${servicesDir}    ${CURDIR}/services
    Set Test Variable    ${resourceDir}    ${CURDIR}/specs
    Create Directory    ${modulesDir}
    Create Directory    ${resourceDir}
    Create Directory    ${routesDir}
    Create Directory    ${servicesDir}
    Create Application And Product

Create All Service File
    ${random} =    Generate Random String    5    [LETTERS]
    ${resource} =    catenate  SEPARATOR=\n
    ...    ---\n
    ...        ${random}:\n
    ...          allowed: []\n
    ...          format: string\n
    ...          settable: false\n
    ...          unit: ''
    ${scripts} =    print("${random}")
    ${resourceContent} =    To Json    {"format":"string","settable":false,"unit":"","allowed":[]}
    Create Specified Data File    resources.yaml    ${CURDIR}/specs    ${resource}
    Create Specified Data File    ${random}.lua    ${CURDIR}/modules    ${scripts}
    Create Specified Data File    ${random}.get.lua    ${CURDIR}/routes    ${scripts}
    Create Specified Data File    {product.id}_event.lua    ${CURDIR}/services    ${scripts}
    Set Test Variable    ${random}
    Set Test Variable    ${resourceContent}

    # verify resource  ExoAdc
    get_solution_all_device_info_via_api    projectId
    # verify modules
    get_module_list    solutionId
    #verify endpoint SolutionSolutionIdEndpoint.py
    solution_solutionID_endpoint_get    solutionID
    #verify services
    get_serviceconfig_via_api    solutionID


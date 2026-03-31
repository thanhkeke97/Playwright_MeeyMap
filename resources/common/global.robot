*** Settings ***
Library    ${EXECDIR}/core/CustomLibrary.py
Library    Browser
Library    Collections
Library    ${EXECDIR}/core/JiraOnlyManager.py    WITH NAME    Jira
Library    ${EXECDIR}/core/PlaywrightHelper.py    WITH NAME    Playwright
Resource    ${EXECDIR}/core/common/utils.robot
Resource    ${EXECDIR}/config/envi.robot
Resource    ${EXECDIR}/keywords/api/authentication.robot


*** Variables ***
${CONFIG_FILE}    ${EXECDIR}/config/ui.yaml
${ENV}    stg
${ENVIRONMENTRUN}    {}

*** Keywords ***
Load config
    ${config}    Load Yaml config    ${CONFIG_FILE}
    ${env_config}    Get From Dictionary    ${config}    ${ENV}
    IF    $ENV == "dev"
        Set Global Variable    ${USERNAME_ADMIN}       admin 
        Set Global Variable    ${PASSWORD_ADMIN}       rDC4MgRnyHjjtNvhZj2zqaJQGgTgM8dnbC3Gkc7eLiU=
    ELSE IF    $ENV == "stg"
        Set Global Variable    ${USERNAME_ADMIN}       admin 
        Set Global Variable    ${PASSWORD_ADMIN}       rDC4MgRnyHjjtNvhZj2zqaJQGgTgM8dnbC3Gkc7eLiU=
    END
    
    Set Global Variable    ${ENVIRONMENTRUN}    ${env_config}

Setup Test Suite
    [Arguments]    @{keywords}
    Log To Console    StatusLogger____${SUITE NAME}____START____    #Must be on top! Do not remove!
    Import Resource    ${EXECDIR}/core/common/utils.robot
    ${length}    Get Length    ${keywords}
    Set Suite Variable    ${length_keyword}    ${length}
    ${download_dir}    Run Keyword If    ${length} > 0    Set Variable    ${keywords[-1]}
    ...    ELSE    Set Variable    ${EMPTY}
    Init Test Environment    ${download_dir}
    MEEY Get All Keywords Setup & Teardown Testcase
    Set Suite Variable    @{refresh_keyword}    Reload
    MEEY Check And Run Keyword    _SetupS

Setup Test Case
    [Arguments]    @{keywords}
    Log To Console    StatusLogger____${SUITE NAME}____${TEST NAME}____START____    #Must be on top! Do not remove!
    Set Test Variable    @{LIST_ERROR}    @{EMPTY}
    ${length}    Get Length    ${keywords}
    Set Test Variable    ${length_keyword}    ${length}
    Set Suite Variable    @{setup_test_keywords}    @{keywords}
    IF    ${length}>0
        FOR    ${keyword}    IN    @{keywords}
            Wait Until Keyword Succeeds    3 times    0.5s    Run Keyword    ${keyword}
        END
    END
    #Tìm trong list setup test case keyword, nếu có trong list thì run kw
    ${setup_keyword}    MEEY Get Keyword Setup|Teardown Testcase    ${setup_tc_keywords}
    Run Keyword If    '${setup_keyword}'!='${EMPTY}'    ${setup_keyword}

Teardown Test Suite
    MEEY Check And Run Keyword    _TeardownS
    # Take Screenshot    ${SCREENSHOT_DIR}/${PREV_TEST_NAME}.png
    ${trace_path}      Set Variable    ${TRACE_DIR}/${PREV_TEST_NAME}_trace.zip
    Close Browser    ALL   
    Log To Console    StatusLogger____${SUITE NAME}____${SUITE STATUS}____    #Must be at bottom! Do not remove!

Teardown Test Case
    Run Keyword And Ignore Error    Empty Directory    ${global_download_dir}
    #Tìm trong list teardown test case keyword, nếu có trong list thì run kw
    ${teardown_keyword}    MEEY Get Keyword Setup|Teardown Testcase    ${teardown_tc_keywords}
    ${test_status}    Set Variable    ${TEST STATUS}
    ${test_message}    Set Variable    ${TEST MESSAGE}
    
    # IF    "${test_status}" == "FAIL"  
    #     Handle Test Fail    ${test_message}
    # END
    Close Browser    CURRENT
    Run Keyword If    '${teardown_keyword}'!='${EMPTY}'    ${teardown_keyword}
    Close Browser    CURRENT
    Log To Console    StatusLogger____${SUITE NAME}____${TEST NAME}____${TEST STATUS}____    #Must be at bottom! Do not remove!

Handle Test Fail
    [Arguments]    ${err_message}
    ${page_details}    Playwright.Get Page Details   
    # ${screenshot_path}    Playwright.Take Screenshot    name=${TEST NAME}
    ${screenshot_path}    Set Variable   ${EXECDIR}/results/ui/screenshots/${TEST NAME}.png
    ${jira_bug}    Set Variable   ${EXECDIR}/results/ui/jira.txt    
    Browser.Take Screenshot    ${screenshot_path}
    Log    message=Test jira
    ${result}    Jira.Handle Bug Lifecycle
    ...    test_name=${TEST_NAME}
    ...    error_message=${err_message}
    ...    page_details=${page_details}
    ...    screenshot_path=${screenshot_path}
    ...    bug_des=${TEST_DOCUMENTATION}
    ...    jira_bug=${jira_bug}

    Log    FINAL RESULT: ${result}    level=INFO
*** Variables ***
# Testsuite
${username_meeyland}              0986668888
${password_meeyland}              12345678
${display_name}                   098666****
${email_meeyland}                 automation_test_team@meeyland.com
# ${tai_khoan_F1_1}               0901231233
# ${tai_khoan_F1_2}               0911231233
# ${tai_khoan_F1_3}               0921231233
# ${tai_khoan_F1_4}               0941231233
# ${tai_khoan_F1_5}               0961231233
# ${tai_khoan_F1_6}               0971231233
# ${tai_khoan_F1_7}               0991231233
# ${tai_khoan_F2}                 0921239999
# ${tai_khoan_F1_chuyen_cay}      0921238888

# ${tai_khoan_F0a}                0931119999
# ${tai_khoan_F1a_1}              0931119998

# ${tai_khoan_F0b}                0932229999
# ${tai_khoan_F1b_1}              0932229998

# ${tai_khoan_F0c}                0933339999
# ${tai_khoan_F1c_1}              0933339998

# ${tai_khoan_F0d}                0934449999
# ${tai_khoan_F1d_1}              0934449998

*** Keywords ***
Init Login Variables
    Set Suite Variable    ${USER_NAME}   ${username_meeyland}
    Set Suite Variable    ${PASSWORD}    ${password_meeyland}
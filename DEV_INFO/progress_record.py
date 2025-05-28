# Latest release
def _v4_0_0_beta_1():
    # py files
    msg_handler      = 2961
    main             = 4391
    input_gui        = 8956
    github_client    = 2897
    font_loader      = 5147
    data_handler     = 5183
    custom_exception = 430
    constants        = 765

    file_count       = 8

    character_count  = msg_handler + main + input_gui + github_client + font_loader + data_handler + custom_exception + constants
    print(f"v4.0.0-beta.1 character count: {character_count}")
    print(f"File count: {file_count}\n")


def _v4_0_0_beta():
    # py files
    msg_handler      = 2961
    main             = 4391
    input_gui        = 8956
    github_client    = 2896
    font_loader      = 5147
    data_handler     = 5163
    custom_exception = 430
    constants        = 763

    file_count       = 8

    character_count  = msg_handler + main + input_gui + github_client + font_loader + data_handler + custom_exception + constants
    print(f"v4.0.0-beta character count: {character_count}")
    print(f"File count: {file_count}\n")

# Right before v4 beta series
def _v4_0_0_alpha_3():
    # py files
    msg_handler      = 2961
    main             = 4435
    input_gui        = 9077
    github_client    = 2938
    font_loader      = 5147
    data_handler     = 3398
    custom_exception = 430
    constants        = 766

    file_count       = 8

    character_count  = msg_handler + main + input_gui + github_client + font_loader + data_handler + custom_exception + constants
    print(f"v4.0.0-alpha.3 character count: {character_count}")
    print(f"File count: {file_count}\n")

def _v4_0_0_alpha_2():
    print(f"v4.0.0-alpha.1 character count: N/A")
    print(f"File count: N/A\n")

def _v4_0_0_alpha_1():
    print(f"v4.0.0-alpha.1 character count: N/A")
    print(f"File count: N/A\n")


def _v4_0_0_alpha():
    # py files
    main             = 2440
    input_gui        = 7382
    github_client    = 2721
    data_handler     = 2714

    file_count       = 4

    character_count  = main + input_gui + github_client + data_handler
    print(f"v4.0.0-alpha character count: {character_count}")
    print(f"File count: {file_count}\n")

# Right before v4 alpha series
def _v3_0_1():
    # py files
    main             = 2238
    input_handler    = 3898
    github_client    = 2372
    data_handler     = 2714

    file_count       = 4

    character_count  = main + input_handler + github_client + data_handler
    print(f"v3.0.1 character count: {character_count}")
    print(f"File count: {file_count}\n")


def _v3_0_0():
    # py files
    main             = 2226
    input_handler    = 3887
    github_client    = 2340
    data_handler     = 2714

    file_count       = 4

    character_count  = main + input_handler + github_client + data_handler
    print(f"v3.0.0 character count: {character_count}")
    print(f"File count: {file_count}\n")

# Right before v3 series
def _v2_0_0():
    # py files
    main             = 8259

    file_count       = 1

    character_count = main
    print(f"v2.0.0 character count: {character_count}")
    print(f"File count: {file_count}\n")

# Right before v2 series
def _v1_2_1():
    # py files
    main             = 5988

    file_count       = 1

    character_count = main
    print(f"v1.2.1 character count: {character_count}")
    print(f"File count: {file_count}\n")


def _v1_2_0():
    # py files
    main             = 5082

    file_count       = 1

    character_count = main
    print(f"v1.2.0 character count: {character_count}")
    print(f"File count: {file_count}\n")


def _v1_1_0():
    # py files
    main             = 4138

    file_count       = 1

    character_count = main
    print(f"v1.1.0 character count: {character_count}")
    print(f"File count: {file_count}\n")

# First release/version
def _v1_0_0():
    # py files
    main             = 1840

    file_count       = 1

    character_count = main
    print(f"v1.0.0 character count: {character_count}")
    print(f"File count: {file_count}\n")


_v4_0_0_beta_1()
_v4_0_0_beta()

print("-"*20)

_v4_0_0_alpha_3()
_v4_0_0_alpha_2()
_v4_0_0_alpha_1()
_v4_0_0_alpha()

print("-"*20)

_v3_0_1()
_v3_0_0()

print("-"*20)

_v2_0_0()

print("-"*20)

_v1_2_1()
_v1_2_0()
_v1_1_0()
_v1_0_0()


""" Output:

v4.0.0-beta.1 character count: 30730
File count: 8

v4.0.0-beta character count: 30707
File count: 8

--------------------
v4.0.0-alpha.3 character count: 29152
File count: 8

v4.0.0-alpha.1 character count: N/A
File count: N/A

v4.0.0-alpha.1 character count: N/A
File count: N/A

v4.0.0-alpha character count: 15257
File count: 4

--------------------
v3.0.1 character count: 11222
File count: 4

v3.0.0 character count: 11167
File count: 4

--------------------
v2.0.0 character count: 8259
File count: 1

--------------------
v1.2.1 character count: 5988
File count: 1

v1.2.0 character count: 5082
File count: 1

v1.1.0 character count: 4138
File count: 1

v1.0.0 character count: 1840
File count: 1

"""
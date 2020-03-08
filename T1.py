# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from enum import Enum
import os

class Token:
    class Type(Enum):
        Error               = -1
        Keyword             = 0
        Identifier          = 1
        Operator            = 2
        Numeric_Literal     = 3
        Character_Literal   = 4
        String_Literal      = 5
        Punctuator          = 6
        Comment             = 7

    def __init__(self, type: Type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "{:17} - {}".format(self.type.name, self.value)

class Transition:
    def __init__(self, src, dst, check, skip = False):
        self.src = src
        self.dst = dst

        self.check_str = check
        self.check = lambda x: eval(self.check_str)

        self.skip = skip

    def __str__(self):
        return "{} --|{}|--> {}".format(self.src, self.check_str, self.dst)

class State:
    def __init__(self, name = "undefined", end = False, dead_end = False, token_type = None):
        self.name = name
        self.end = end
        self.dead_end = dead_end
        self.token_type = token_type
    def __str__(self):
        if self.end:
            return "[{}]".format(self.name)
        else:
            return "({})".format(self.name)


# %%
'''
    States
'''
# General
s_start                      = State("Start")
s_punctuators                = State("Punctuator",                 end=True, token_type=Token.Type.Punctuator, dead_end=True)

# Comments
s_comment_singleline         = State("Comment singleline",         end=True, token_type=Token.Type.Comment)
# s_comment_singleline_exit    = State("Comment singleline exit",    end=True, token_type=Token.Type.Comment, dead_end=True)
s_comment_multiline          = State("Comment multiline",                    token_type=Token.Type.Comment)
s_comment_multiline_exit_1   = State("Comment multiline exit (*)",           token_type=Token.Type.Comment)
s_comment_multiline_exit_2   = State("Comment multiline exit (/)", end=True, token_type=Token.Type.Comment, dead_end=True)

# Operators
s_plus                       = State("Plus",                       end=True, token_type=Token.Type.Operator)
s_minus                      = State("Minus",                      end=True, token_type=Token.Type.Operator)
s_slash                      = State("Slash",                      end=True, token_type=Token.Type.Operator)
s_asterisk                   = State("Asterisk",                   end=True, token_type=Token.Type.Operator)
s_modulo                     = State("Modulo",                     end=True, token_type=Token.Type.Operator)
s_increment                  = State("Increment",                  end=True, token_type=Token.Type.Operator, dead_end=True)
s_decrement                  = State("Decrement",                  end=True, token_type=Token.Type.Operator, dead_end=True)

s_equal                      = State("Equal",                      end=True, token_type=Token.Type.Operator, dead_end=True)
s_different                  = State("Different",                  end=True, token_type=Token.Type.Operator, dead_end=True)
s_greater                    = State("Greater",                    end=True, token_type=Token.Type.Operator)
s_less                       = State("Less",                       end=True, token_type=Token.Type.Operator)
s_greater_equal              = State("Greater or equal",           end=True, token_type=Token.Type.Operator, dead_end=True)
s_less_equal                 = State("Less or equal",              end=True, token_type=Token.Type.Operator, dead_end=True)

s_and                        = State("And",                        end=True, token_type=Token.Type.Operator, dead_end=True)
s_or                         = State("Or",                         end=True, token_type=Token.Type.Operator, dead_end=True)
s_not                        = State("Not",                        end=True, token_type=Token.Type.Operator)

s_bitwise_left_shift         = State("Bitwise left shift",         end=True, token_type=Token.Type.Operator)
s_bitwise_right_shift        = State("Bitwise right shift",        end=True, token_type=Token.Type.Operator)
s_bitwise_not                = State("Bitwise not",                end=True, token_type=Token.Type.Operator)
s_bitwise_and                = State("Bitwise and",                end=True, token_type=Token.Type.Operator)
s_bitwise_or                 = State("Bitwise or",                 end=True, token_type=Token.Type.Operator)
s_bitwise_xor                = State("Bitwise xor",                end=True, token_type=Token.Type.Operator)

s_assign                     = State("Assign",                     end=True, token_type=Token.Type.Operator)
s_increment_assign           = State("Increment assign",           end=True, token_type=Token.Type.Operator, dead_end=True)
s_decrement_assign           = State("Decrement assign",           end=True, token_type=Token.Type.Operator, dead_end=True)
s_multiply_assign            = State("Multiply assign",            end=True, token_type=Token.Type.Operator, dead_end=True)
s_divide_assign              = State("Divide assign",              end=True, token_type=Token.Type.Operator, dead_end=True)
s_modulo_assign              = State("Modulo assign",              end=True, token_type=Token.Type.Operator, dead_end=True)
s_bitwise_left_shift_assign  = State("Biwtise shift left assign",  end=True, token_type=Token.Type.Operator, dead_end=True)
s_bitwise_right_shift_assign = State("Bitwise shift right assign", end=True, token_type=Token.Type.Operator, dead_end=True)
s_bitwise_and_assign         = State("Bitwise and assign",         end=True, token_type=Token.Type.Operator, dead_end=True)
s_bitwise_or_assign          = State("Bitwise or assign",          end=True, token_type=Token.Type.Operator, dead_end=True)
s_bitwise_xor_assign         = State("Bitwise xor assign",         end=True, token_type=Token.Type.Operator, dead_end=True)

s_arrow                      = State("Arrow",                      end=True, token_type=Token.Type.Operator, dead_end=True)

# Identifiers
s_identifier_first_letter    = State("Identifier first letter",    end=True, token_type=Token.Type.Identifier)
s_identifier                 = State("Identifier",                 end=True, token_type=Token.Type.Identifier)

# Character Literals
s_character_open             = State("Character open")
s_character                  = State("Character")
s_character_close            = State("Character",                  end=True, token_type=Token.Type.Character_Literal, dead_end=True)
s_character_escape_backslash = State("Escape character backslash")
s_character_escape           = State("Escape character")
s_character_escape_close     = State("Escape character",          end=True, token_type=Token.Type.Character_Literal, dead_end=True)

# String Literals
s_string_open                = State("String open",                         token_type=Token.Type.String_Literal)
s_string                     = State("String",                              token_type=Token.Type.String_Literal)
s_string_escape_backslash    = State("String escape character backslash",   token_type=Token.Type.String_Literal)
s_string_escape              = State("String escape character",             token_type=Token.Type.String_Literal)
s_string_close               = State("String",                    end=True, token_type=Token.Type.String_Literal, dead_end=True)
s_string_newline             = State("String newline",                      token_type=Token.Type.String_Literal)

# Numbers
# s_number_sign                = State("Number sign")
# s_number_sign_minus          = State("Number sign minus")
# s_number_sign_plus           = State("Number sign plus")
s_number_integer             = State("Number integer",   end=True, token_type=Token.Type.Numeric_Literal)
s_number_real_point          = State("Number real point")
s_number_real                = State("Number real",      end=True, token_type=Token.Type.Numeric_Literal)
s_number_suffixed            = State("Number suffixed",  end=True, token_type=Token.Type.Numeric_Literal, dead_end=True)
s_number_exponent_e          = State("Number exponent e")
s_number_exponent_sign       = State("Number exponent sign")
s_number_exponent            = State("Number exponent",  end=True, token_type=Token.Type.Numeric_Literal)



'''
    Transitions
'''
# Whitespace
t_whitespace                  = Transition(s_start,                       s_start,                     "x in Scanner.WHITESPACE", skip=True)

# Punctuators
t_punctuators                 = Transition(s_start,                       s_punctuators,              "x in Scanner.PUNCTUATORS")

# Comments
'''
# Test transitions
t_comment_singleline          = Transition(s_slash,                       s_comment_singleline,         "x == '/'")
t_comment_singleline_content  = Transition(s_comment_singleline,          s_comment_singleline,         "x != '\\n'")
# t_comment_singleline_exit     = Transition(s_comment_singleline,          s_comment_singleline_exit,    "x == '\\n'")
t_comment_multiline           = Transition(s_slash,                       s_comment_multiline,          "x == '*'")
t_comment_multiline_content   = Transition(s_comment_multiline,           s_comment_multiline,          "x != '*'")
t_comment_multiline_exit_1    = Transition(s_comment_multiline,           s_comment_multiline_exit_1,   "x == '*'")
t_comment_multiline_continue  = Transition(s_comment_multiline_exit_1,    s_comment_multiline,          "x != '/'")
t_comment_multiline_exit_2    = Transition(s_comment_multiline_exit_1,    s_comment_multiline_exit_2,   "x == '/'")
'''
t_comment_singleline          = Transition(s_slash,                       s_comment_singleline,         "x == '/'",   skip=True)
t_comment_singleline_content  = Transition(s_comment_singleline,          s_comment_singleline,         "x != '\\n'", skip=True)
t_comment_singleline_ignore   = Transition(s_comment_singleline,          s_start,                      "x == '\\n'", skip=True)
t_comment_multiline           = Transition(s_slash,                       s_comment_multiline,          "x == '*'",   skip=True)
t_comment_multiline_content   = Transition(s_comment_multiline,           s_comment_multiline,          "x != '*'",   skip=True)
t_comment_multiline_exit_1    = Transition(s_comment_multiline,           s_comment_multiline_exit_1,   "x == '*'",   skip=True)
t_comment_multiline_exit_loop = Transition(s_comment_multiline_exit_1,    s_comment_multiline_exit_1,   "x == '*'",   skip=True)
t_comment_multiline_ignore    = Transition(s_comment_multiline_exit_1,    s_start,                      "x == '/'",   skip=True)
t_comment_multiline_continue  = Transition(s_comment_multiline_exit_1,    s_comment_multiline,          "x != '/'",   skip=True)

# Operators
t_plus                        = Transition(s_start,                       s_plus,                       "x == '+'")
t_minus                       = Transition(s_start,                       s_minus,                      "x == '-'")
t_multiply                    = Transition(s_start,                       s_asterisk,                   "x == '*'")
t_divide                      = Transition(s_start,                       s_slash,                      "x == '/'")
t_modulo                      = Transition(s_start,                       s_modulo,                     "x == '%'")
t_increment                   = Transition(s_plus,                        s_increment,                  "x == '+'")
t_decrement                   = Transition(s_minus,                       s_decrement,                  "x == '-'")

t_equal                       = Transition(s_assign,                      s_equal,                      "x == '='")
t_different                   = Transition(s_not,                         s_different,                  "x == '='")
t_greater                     = Transition(s_start,                       s_greater,                    "x == '>'")
t_less                        = Transition(s_start,                       s_less,                       "x == '<'")
t_greater_equal               = Transition(s_greater,                     s_greater_equal,              "x == '='")
t_less_equal                  = Transition(s_less,                        s_less_equal,                 "x == '='")

t_not                         = Transition(s_start,                       s_not,                        "x == '!'")
t_and                         = Transition(s_bitwise_and,                 s_and,                        "x == '&'")
t_or                          = Transition(s_bitwise_or,                  s_or,                         "x == '|'")

t_bitwise_left_shift          = Transition(s_less,                        s_bitwise_left_shift,         "x == '<'")
t_bitwise_right_shift         = Transition(s_greater,                     s_bitwise_right_shift,        "x == '>'")
t_bitwise_not                 = Transition(s_start,                       s_bitwise_not,                "x == '~'")
t_bitwise_and                 = Transition(s_start,                       s_bitwise_and,                "x == '&'")
t_bitwise_or                  = Transition(s_start,                       s_bitwise_or,                 "x == '|'")
t_bitwise_xor                 = Transition(s_start,                       s_bitwise_xor,                "x == '^'")

t_assign                      = Transition(s_start,                       s_assign,                     "x == '='")
t_increment_assign            = Transition(s_minus,                       s_increment_assign,           "x == '='")
t_decrement_assign            = Transition(s_plus,                        s_decrement_assign,           "x == '='")
t_multiply_assign             = Transition(s_asterisk,                    s_multiply_assign,            "x == '='")
t_divide_assign               = Transition(s_slash,                       s_divide_assign,              "x == '='")
t_modulo_assign               = Transition(s_modulo,                      s_modulo_assign,              "x == '='")
t_bitwise_left_shift_assign   = Transition(s_bitwise_left_shift,          s_bitwise_left_shift_assign,  "x == '='")
t_bitwise_right_shift_assign  = Transition(s_bitwise_right_shift,         s_bitwise_right_shift_assign, "x == '='")
t_bitwise_and_assign          = Transition(s_bitwise_and,                 s_bitwise_and_assign,         "x == '='")
t_bitwise_or_assign           = Transition(s_bitwise_or,                  s_bitwise_or_assign,          "x == '='")
t_bitwise_xor_assign          = Transition(s_bitwise_xor,                 s_bitwise_xor_assign,         "x == '='")

t_arrow                       = Transition(s_minus,                       s_arrow,                      "x == '>'")

# Identifiers
t_identifier_first_letter     = Transition(s_start,                       s_identifier_first_letter,    "x in Scanner.VALID_FIRST_CHARACTERS")
t_identifier_letters          = Transition(s_identifier_first_letter,     s_identifier,                 "x in Scanner.VALID_CHARACTERS")
t_identifier_letters_2        = Transition(s_identifier,                  s_identifier,                 "x in Scanner.VALID_CHARACTERS")

# Character Literals
t_character_open              = Transition(s_start,                       s_character_open,             "x == '\\\''")
t_character                   = Transition(s_character_open,              s_character,                  "x in Scanner.VALID_CHARACTERS")
t_character_close             = Transition(s_character,                   s_character_close,            "x == '\\\''")
t_character_escape_backslash  = Transition(s_character_open,              s_character_escape_backslash, "x == '\\\\\'")
t_character_escape            = Transition(s_character_escape_backslash,  s_character_escape,           "x in Scanner.VALID_ESCAPE_CHARACTERS")
t_character_escape_close      = Transition(s_character_escape,            s_character_close,            "x == '\\\''")

# String Literals
t_string_open                 = Transition(s_start,                       s_string_open,                "x == '\\\"'")
t_string_close_empty          = Transition(s_string_open,                 s_string_close,               "x == '\\\"'")
t_string                      = Transition(s_string_open,                 s_string,                     "x in Scanner.VALID_STRING_CHARACTERS")
t_string_content              = Transition(s_string,                      s_string,                     "x in Scanner.VALID_STRING_CHARACTERS")
t_string_close                = Transition(s_string,                      s_string_close,               "x == '\\\"'")
t_string_escape_first         = Transition(s_string_open,                 s_string_escape_backslash,    "x == '\\\\\'")
t_string_escape_backslash     = Transition(s_string,                      s_string_escape_backslash,    "x == '\\\\\'")
t_string_escape               = Transition(s_string_escape_backslash,     s_string_escape,              "x in Scanner.VALID_ESCAPE_CHARACTERS")
t_string_escape_close         = Transition(s_string_escape,               s_string_close,               "x == '\\\"'")
t_string_escape_back          = Transition(s_string_escape,               s_string,                     "x in Scanner.VALID_STRING_CHARACTERS")
t_string_escape_back_escape   = Transition(s_string_escape,               s_string_escape_backslash,    "x in Scanner.VALID_ESCAPE_CHARACTERS")
t_string_newline              = Transition(s_string_escape_backslash,     s_string_newline,             "x == '\\n'")
t_string_newline_back         = Transition(s_string_newline,              s_string,                     "x in Scanner.VALID_STRING_CHARACTERS")
t_string_newline_back_escape  = Transition(s_string_newline,              s_string_escape_backslash,    "x == '\\\\\'")
t_string_newline_close        = Transition(s_string_newline,              s_string_close,               "x == '\\\"'")

# Numbers
# t_number_sign                = Transition(s_start,                s_number_sign,          "x == '-' or x == '+'")
# t_number_sign_minus          = Transition(s_minus,                s_number_sign_minus,    "x == '-'")
# t_number_sign_plus           = Transition(s_plus,                 s_number_sign_plus,     "x == '+'")
t_number_integer             = Transition(s_start,                s_number_integer,       "x.isdigit()") # and x != 0")
t_number_real_point          = Transition(s_start,                s_number_real_point,    "x == '.'")
# t_number_sign_integer        = Transition(s_number_sign,          s_number_integer,       "x.isdigit()")
t_number_sign_minus_integer  = Transition(s_minus,                s_number_integer,       "x.isdigit()")
t_number_sign_plus_integer   = Transition(s_plus,                 s_number_integer,       "x.isdigit()")
# t_number_sign_real           = Transition(s_number_sign,          s_number_real_point,    "x == '.'")
t_number_sign_minus_real     = Transition(s_minus,                s_number_real_point,    "x == '.'")
t_number_sign_plus_real      = Transition(s_plus,                 s_number_real_point,    "x == '.'")
t_number_integer_integer     = Transition(s_number_integer,       s_number_integer,       "x.isdigit()")
t_number_integer_point       = Transition(s_number_integer,       s_number_real_point,    "x == '.'")
t_number_real_point_real     = Transition(s_number_real_point,    s_number_real,          "x.isdigit()")
t_number_real_real           = Transition(s_number_real,          s_number_real,          "x.isdigit()")
t_number_integer_suffix      = Transition(s_number_integer,       s_number_suffixed,      "x in Scanner.NUMBER_SUFFIXES")
t_number_real_suffix         = Transition(s_number_real,          s_number_suffixed,      "x in Scanner.NUMBER_SUFFIXES")
t_number_integer_exponent_e  = Transition(s_number_integer,       s_number_exponent_e,    "x in Scanner.NUMBER_EXPONENT")
t_number_real_exponent_e     = Transition(s_number_real,          s_number_exponent_e,    "x in Scanner.NUMBER_EXPONENT")
t_number_exponent            = Transition(s_number_exponent_e,    s_number_exponent,      "x.isdigit()")
t_number_exponent_sign       = Transition(s_number_exponent_e,    s_number_exponent_sign, "x == '-' or x == '+'")
t_number_exponent_signed     = Transition(s_number_exponent_sign, s_number_exponent,      "x.isdigit()")
t_number_exponent_exponent   = Transition(s_number_exponent,      s_number_exponent,      "x.isdigit()")

state_list = [
    s_start, s_punctuators,
    s_comment_singleline, s_comment_multiline, s_comment_multiline_exit_1, s_comment_multiline_exit_2,
    s_plus, s_minus, s_asterisk, s_slash, s_modulo, s_increment, s_decrement,
    s_equal, s_different, s_greater, s_less, s_greater_equal, s_less_equal,
    s_and, s_or, s_not,
    s_bitwise_left_shift, s_bitwise_right_shift, s_bitwise_not, s_bitwise_and, s_bitwise_or, s_bitwise_xor,
    s_assign, s_increment_assign, s_decrement_assign, s_multiply_assign, s_divide_assign, s_modulo_assign, s_bitwise_left_shift_assign, s_bitwise_right_shift_assign, s_bitwise_and_assign, s_bitwise_or_assign, s_bitwise_xor_assign,
    s_identifier_first_letter, s_identifier,
    s_character_open, s_character, s_character_close, s_character_escape_backslash, s_character_escape, s_character_escape_close,
    s_string_open, s_string, s_string_escape_backslash, s_string_escape, s_string_close, s_string_newline,
    s_number_integer, s_number_real_point, s_number_real, s_number_suffixed, s_number_exponent_e, s_number_exponent_sign, s_number_exponent,
]

transition_list = [
    t_whitespace,
    t_punctuators,
    t_comment_singleline, t_comment_singleline_content, t_comment_singleline_ignore, t_comment_multiline, t_comment_multiline_content, t_comment_multiline_exit_1, t_comment_multiline_exit_loop, t_comment_multiline_ignore, t_comment_multiline_continue, t_equal, t_different, t_greater, t_less, t_greater_equal, t_less_equal,
    t_plus, t_minus, t_multiply, t_divide, t_modulo, t_increment, t_decrement,
    t_equal, t_different, t_greater, t_less, t_greater_equal, t_less_equal,
    t_not, t_and, t_or,
    t_bitwise_left_shift, t_bitwise_right_shift, t_bitwise_not, t_bitwise_and, t_bitwise_or, t_bitwise_xor,
    t_assign, t_increment_assign, t_decrement_assign, t_multiply_assign, t_divide_assign, t_modulo_assign, t_bitwise_left_shift_assign, t_bitwise_right_shift_assign, t_bitwise_and_assign, t_bitwise_or_assign, t_bitwise_xor_assign,
    t_identifier_first_letter, t_identifier_letters, t_identifier_letters_2,
    t_character_open, t_character, t_character_close, t_character_escape_backslash, t_character_escape, t_character_escape_close,
    t_string_open, t_string_close_empty, t_string, t_string_content, t_string_close, t_string_escape_first, t_string_escape_backslash, t_string_escape, t_string_escape_close, t_string_escape_back, t_string_escape_back_escape, t_string_newline, t_string_newline_back, t_string_newline_back_escape, t_string_newline_close,
    t_number_integer, t_number_real_point, t_number_sign_minus_integer, t_number_sign_plus_integer, t_number_sign_minus_real, t_number_sign_plus_real, t_number_integer_integer, t_number_integer_point, t_number_real_point_real, t_number_real_real, t_number_integer_suffix, t_number_real_suffix, t_number_integer_exponent_e, t_number_real_exponent_e, t_number_exponent, t_number_exponent_sign, t_number_exponent_signed, t_number_exponent_exponent,
]


# %%
class Scanner:
    WHITESPACE = [
        ' ', '\t', '\n', '',
    ]
    KEYWORDS = [
        "auto",     "break",        "case",     "char",     "const",        "continue",     "default",      "do",
        "double",   "else",         "enum",     "extern",   "float",        "for",          "goto",         "if",
        "int",      "long",         "register", "return",   "short",        "signed",       "sizeof",       "static",
        "struct",   "switch",       "typedef",  "union",    "unsigned",     "void",         "volatile",     "while",
    ]
    OPERATORS = [
        "+",    "-",    "*",    "/",    "%",    "++",   "--",                                   # Arithmetic Operators
        "==",   "!=",   ">",    "<",    ">=",   "<=",                                           # Relational Operators
        "&&",   "||",   "!",                                                                    # Logical Operators
        "<<",   ">>",   "~",    "&",    "^",    "|",                                            # Bitwise Operators
        "=",    "+=",   "-=",   "*=",   "/=",   "%=",   "<<=",  ">>=",  "&=",   "^=",   "|=",   # Assignment Operators
        "->",
    ]
    PUNCTUATORS = [
         ",",#    ".",
         ":",    ";",
         "(",    ")",    "{",    "}",    "[",    "]",
         "#",    # "##",
    ]
    VALID_FIRST_CHARACTERS    = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
    VALID_CHARACTERS          = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789"
    VALID_STRING_CHARACTERS   = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789 ~!@#$%^&*()_+{}|:<>?[];',./'"
    INVALID_STRING_CHARACTERS = "\\\"\n"
    VALID_ESCAPE_CHARACTERS   = "abefnrtv\\\'\"?\""
    NUMBER_SUFFIXES           = "lLfF"
    NUMBER_EXPONENT           = "eE"
    def __init__(self, file_path, state_list = [], transition_list = []):
        self.file = open(file_path, "r")
        # self.file_text = self.file.read()
        self.state_list = state_list
        self.transition_list = transition_list

        # self.current_line = None
        self.line_number = 1
        self.token_line_number = 1
        self.token_start_position = 0

        self.string_table = []
        self.current_character = ''
        self.current_state = self.state_list[0]
        self.current_token_value = ""

    def add_string(self, string):
        if string not in self.string_table:
            self.string_table.append(string)
        return self.string_table.index(string)

    def make_token(self):
        if self.current_character == '' and self.current_token_value == '':
            return 'EOF'
        else:
            if self.current_state.end:
                if self.current_character != '':
                    self.file.seek(self.file.tell() - 1)
                if self.current_state.token_type == Token.Type.String_Literal:
                    pos = self.add_string(self.current_token_value)
                    return Token(self.current_state.token_type, pos)
                if self.current_token_value in Scanner.KEYWORDS:
                    return Token(Token.Type.Keyword, self.current_token_value.rstrip())
                    # return Token(Token.Type.Keyword, "{:10} ({})".format(self.current_token_value.rstrip(), "Keyword"))
                else:
                    return Token(self.current_state.token_type, self.current_token_value.rstrip())
                    # return Token(self.current_state.token_type, "{:10} ({})".format(self.current_token_value.rstrip(), str(self.current_state.name)))
            else:
                self.current_token_value += self.current_character
                return Token(Token.Type.Error, "Position in file: {}, Line: {} - {}".format(
                        self.token_start_position, #self.file.tell(),
                        self.token_line_number, #self.line_number,
                        repr(self.current_token_value) + "\nState: " + str(self.current_state)
                        ))


    def get_token(self, debug = False):
        self.current_state = self.state_list[0]
        self.current_token_value = ""

        self.token_line_number = self.line_number
        self.token_start_position = self.file.tell()

        while True:
            self.current_character = self.file.read(1)
            if self.current_character == '':
                return self.make_token()

            # print('Current self.current_character: {}'.format(repr(self.current_character)))

            moved = False
            if not self.current_state.dead_end:
                for transition in self.transition_list:
                    if debug:
                        # print("{:28} - {:>5} | {:1} - {:>5} | {}".format(
                        #     str(self.current_state), str(self.current_state == transition.src),
                        #     self.current_character, str(transition.check(self.current_character)),
                        #     transition)
                        # )
                        print("{:>5} | {:>5} | {}".format(
                            str(self.current_state == transition.src),
                            str(transition.check(self.current_character)),
                            transition)
                        )

                    if transition.src == self.current_state and transition.check(self.current_character):
                        # print(transition)

                        # Comment slash fix
                        if (transition.src.token_type == Token.Type.Comment or transition.dst.token_type == Token.Type.Comment) and \
                            transition.src.token_type != transition.dst.token_type:
                            self.current_token_value = self.current_token_value[:-1]

                        self.current_state = transition.dst
                        moved = True

                        if self.current_character == '\n':
                            self.line_number += 1
                            if self.current_token_value == '':
                                self.token_line_number += 1

                        if not transition.skip:
                            self.current_token_value += self.current_character

                        # print(self.current_token_value)
                        break

            if debug:
                print()
            # print(moved)
            if not moved:
                return self.make_token()
            # if self.current_token_value == '':
            #     return self.get_token()


# %%

s = Scanner(
    # "testulet.txt",
    # "test_c1.txt",
    "test_c2.txt",
    # "aici.txt",
    state_list,
    transition_list
    )

output = open("output.txt", "w")

# for i in range(4):
while True:
    token = s.get_token()
    # token = s.get_token(debug=True)
    # print()
    # print(token)

    if token == 'EOF' or token.type == Token.Type.Error:
        output.write(str(token) + "\n")
        break

    if token.type == Token.Type.String_Literal:
        token.value = s.string_table[int(token.value)]
    output.write(str(token) + "\n")

output.close()

# %%

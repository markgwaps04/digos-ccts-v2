import speech_recognition as speech
import difflib
import re;
from pyphonetics import RefinedSoundex, Soundex,Metaphone

class SpeechAnalyzer():

    base = None;

    def __init__(self, AUDIO_FILE):

        try:

            r = speech.Recognizer();
            of_audio = speech.AudioFile(AUDIO_FILE);

            with of_audio as source:
                audio = r.record(source);

            self.__recognized_words__ = r.recognize_google(audio);

        except:
            raise SpeechNotRecognized("No recognized words");
        pass;

    def get_recognized_words(self):
        return self.__recognized_words__;
        pass;

    pass;


class Miscue():

     # (0, 'Mispronunciation'),
     #    (1, 'Omission'),
     #    (2, 'Substitution'),
     #    (3, 'Insertion'),
     #    (4, 'Repetition'),
     #    (5, 'Transposition'),
     #    (6, 'Reversal'),

    __params__ = dict();
    index = None;

    def __init__(self, **params):
        self.__params__ = params;
        self.index = self.__params__["index"];
        pass;

    def get_attributes(self):
        return self.__params__;
        pass;

    def get_info(self):

        recognize = self.__params__["recognize"];
        recognize = "".join(recognize);
        base = self.__params__["base"];

        attributes = {
            "index" : self.__params__["index"],
            "miscue_base" : base,
            "miscue_result" : recognize
        }

        rs = RefinedSoundex();
        soundex = Soundex();

        if str(base).isnumeric() or str(recognize).isnumeric():
            attributes['type'] = 0;
            return attributes;
        else :

            distance = rs.distance(base, recognize);

            sounds = soundex.sounds_like(base, recognize);

            if distance < 1 or sounds :

                attributes['type'] = 0;
                return attributes;

            else:

                attributes['type'] = 2;
                return attributes;

                pass;

        pass;


    pass;


class Recognizer(SpeechAnalyzer):

    __BASE__ = None;
    __TEST__ = None;
    __COMPARE_RESULTS__ = None;
    __GROUPED_RESULTS__ = None;
    __BLOCK_QUE__ = [];
    __POSITION__ = -1;
    parse_value = [];
    error_parse = [];
    miscue = [];
    of_miscue = [];


    def __init__(self, TEST, AUDIO_FILE):

        SpeechAnalyzer.__init__(self, AUDIO_FILE);

        self.__BASE__ = str(TEST).lower();

        self.__TEST__ = str(self.__recognized_words__).lower();

        self.__BASE__ = str(self.__BASE__).replace("\n"," ");

        self.__BASE__ = re.sub(r'[^A-Za-z0-9\s]+', '', self.__BASE__)
        self.__TEST__ = re.sub(r'[^A-Za-z0-9\s]+', '', self.__TEST__);

        self.__BASE__ = re.sub('[^A-z0-9 -]',' ',self.__BASE__);
        self.__TEST__ = re.sub('[^A-z0-9 -]',' ',self.__TEST__);

        # initiate the Differ object
        that_diff = difflib.Differ();

        base_splitted = self.__BASE__.split();
        test_splitted = self.__TEST__.split();

        # calculate the difference between the two texts
        self.__COMPARE_RESULTS__ = that_diff.compare(base_splitted,list(test_splitted));

        self.__COMPARE_RESULTS__ = filter(self.__clean__, list(self.__COMPARE_RESULTS__));
        self.__COMPARE_RESULTS__ = list(self.__COMPARE_RESULTS__);

        self.__GROUPED_RESULTS__ = self.__group_by_correctness__(self.__COMPARE_RESULTS__);

        print(TEST);

        parse = [];
        for index, per in enumerate(self.__GROUPED_RESULTS__) :
            result = self.__align__(per);
            parse = parse + result;
            pass;

        self.parse_value = parse;
        self.__miscue_check__(self.parse_value);

    def __clean__(self,value):
        no_s_characters = ''.join(e for e in value if e.isalnum());
        return len(no_s_characters) > 0;
        pass;

    def __group_by_correctness__(self, COMPARE_RESULTS):

        res = []
        que = False;
        increment_position = -1;
        for index, per in enumerate(COMPARE_RESULTS):
            no_s_characters = ''.join(e for e in per if e.isalnum());
            first_char = str(per)[0] if len(no_s_characters) > 0 else None;
            position = -1;

            if first_char == "-" or ( no_s_characters and first_char != "+" ):
                increment_position +=1;
                position = increment_position;
                pass;

            if len(no_s_characters) <= 0:
                continue;

            if first_char != "-" and first_char != "+":

                obj = {
                    "index" : index,
                    "value" : no_s_characters,
                    "position" : position
                };

                res.append([obj]);
                que = True;
            else:
                last_index = len(res) - 1 if res else None;

                obj = {
                    "index" : index,
                    "value" : str(per).strip(),
                    "position" : position
                };

                if last_index != None and not que:
                    res[last_index].append(obj);
                else:
                    res.append([obj]);

                que = False;

            pass;

        return res;

        pass;

    def __align__(self, GROUPED_RESULTS):

        attributes = {
            "index" : None,
            "base" : None,
            "recognize" : None,
            "type" : None,
            "is_correct" : False,
            "error_parse" : False,
            "nest" : []
        };
        res = [];
        tmp_que = [];
        first_res = None;
        test = False;
        add_plus = [];

        for index,per in enumerate(GROUPED_RESULTS):

            position = per['position'];
            per = per["value"];

            no_s_characters = ''.join(e for e in per if e.isalnum());
            first_char = str(per)[0] if len(no_s_characters) > 0 else None;
            is_empty_que = len(res) <= 0;

            params = attributes.copy();
            params["index"] = position;
            params["base"] = no_s_characters;
            params["recognize"] = [];
            params["type"] = first_char;
            params["portion"] = None;
            params["nest"] = [];
            params["block"] = self.__BLOCK_QUE__.copy();

            params["is_correct"] = True \
                    if first_char != "-" and first_char != "+" \
                    else False;

            params["portion"] = "A";


            if is_empty_que and index == 0 and params['type'] == "-":
                first_res = params.copy();
                tmp_que = params.copy();
                res.append(first_res);
                self.__BLOCK_QUE__ = [];
                continue;
            elif is_empty_que and index == 0 and params['type'] == "+":
                first_res = params.copy();
                tmp_que = params.copy();
                add_plus.append(no_s_characters);
                self.__BLOCK_QUE__.append(no_s_characters);
                continue;
            elif params['type'] != "+" and params['type'] != "-":
                res.append(params.copy());
                self.__BLOCK_QUE__ = [];
                break;
                pass;

            # 2nd loop

            if first_res["type"] == "-" and first_res["is_correct"] == False:
                last_index_que = res[len(res) - 1];
                last_index = len(res) - 1;

                if tmp_que["type"] == "-"  and first_char == "+" or \
                   tmp_que["type"] == "+" and first_char == "+"  :

                    tmp_que = params.copy();
                    res[last_index]["recognize"].append(no_s_characters);
                    continue;

                elif tmp_que["type"] == "+" and first_char == "-":
                    tmp_que = params.copy();
                    res.append(tmp_que);
                    continue;

                elif tmp_que["type"] == "-" and first_char == "-":

                     params["nest"] = params.copy();
                     tmp_que = params["nest"];
                     res[last_index]["nest"].append(tmp_que);
                     continue;

                     pass;

            elif first_res["type"] == "+" and first_res["is_correct"] == False:

                params["portion"] = "B";
                if tmp_que["type"] == "+" and len(res) <= 0:
                    self.__BLOCK_QUE__.append(no_s_characters);
                else:
                    self.__BLOCK_QUE__ = [];
                    pass;

                if tmp_que["type"] == "+"  and first_char == "+":
                    add_plus.append(no_s_characters);
                    tmp_que = params.copy();
                    continue;

                elif tmp_que["type"] == "+" and first_char == "-":

                    if first_res["type"] == "+" and len(params['block']) > 0:
                        params['block'].pop();

                    params["recognize"] = add_plus.copy();
                    tmp_que = params.copy();
                    add_plus = [];
                    res.append(tmp_que);
                    continue;

                elif tmp_que["type"] == "-" and first_char == "+":

                    last_index_que = res[len(res) - 1];
                    last_index = len(res) - 1;

                    tmp_que = params.copy();
                    res[last_index]["recognize"].append(no_s_characters);

                    continue;

                elif tmp_que["type"] == "-" and first_char == "-":

                    last_index_que = res[len(res) - 1];
                    last_index = len(res) - 1;
                    params["nest"] = params.copy();
                    tmp_que = params["nest"];
                    res[last_index]["nest"].append(tmp_que);
                    continue;

                    pass;

            pass;

        return res;

        pass;

    def __miscue_check__(self, parse):

        for index, per in enumerate(parse):
            if per["is_correct"] == False and (len(per["nest"]) > 0 or len(per["recognize"]) <= 0 ):
                per['error_parse'] = True;
                self.error_parse.append(per);
            elif per["is_correct"] == False and len(per["recognize"]) == 1:
                self.miscue.append(Miscue(**per));
                self.of_miscue.append(per);
                pass;

            pass;

        pass;

    pass;

import os
import re
import argparse
import yaml
import spacy
import subprocess

def text_process(texts):
    action_list = []
    mdm_list = []
    condition_list = []
    for text in texts:
        print("Processing: \"{}\"".format(text))
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        word_list = [token.text for token in doc]
        print(word_list)
        subject = []
        background = []
        action = []
        root = ""

        if doc[-2].pos_ == "NOUN":
            if doc[-4].pos_ == "ADP":
                background.append(doc[-4].text)
            if doc[-3].pos_ == "DET":
                background.append(doc[-3].text)
            background.append(doc[-2].text)

        for i, token in enumerate(doc):
            if token.dep_ == "nsubj":
                if doc[i-2].dep_ == "det":
                    subject.append(doc[i-2].text)
                if doc[i-1].dep_ == "compound" or doc[i-1].dep_ == "det":
                    subject.append(doc[i-1].text)
                subject.append(token.text)
           # elif token.dep_ == "prep":
           #     background.append(token.text)
           #     idx = 1
           #     while (doc[i+idx].dep_ != "punct" and doc[i+idx].dep_ != "nsubj"
           #            and doc[i+idx].dep_ != "ROOT" and doc[i+idx].pos_ != "VERB"):
           #         if doc[i+idx].text == "and" and doc[i+idx+1].pos_ == "VERB":
           #             idx += 1
           #             continue
           #         background.append(doc[i+idx].text)
           #         idx += 1
            elif token.dep_ == "ROOT" or token.pos_ == "VERB":
                root = token.text
                action.append(root)

            print(f"{token.text:<20} {token.pos_:<20} "
                  f"{token.dep_:<20} {token.head.text:<20} {token.ent_type_:<20}")

        subject_background = subject + background
        print(subject)
        print(background)
        print(subject_background)
        mdm = [text for text in word_list if text not in subject_background]
        #print(mdm)
        mdm_text = "a person " + " ".join(action)
        follow_text = " ".join(subject_background)
        print("mdm.txt: {}".format(mdm_text))
        print("condition.yaml: {} \n".format(follow_text))

        action_list.append("_".join(action))
        mdm_list.append(mdm_text)
        condition_list.append(follow_text)
    return action_list, mdm_list, condition_list

def run_mdm(model, action_name):
    #output_path = input(f"Provide output folder for mdm [{action_name}?]: ")
    #output_name = input(f"Provide the name of output video (default={action_name}): ")
    working_directory = "/workspace/animation_from_TP/motion-diffusion-model/"
    print("Action: \"{}\" is processing...".format(action_name))
    subprocess.run([f"python -m sample.generate --model_path ./save/humanml_trans_enc_512/model000200000.pt --input_text /workspace/animation_from_TP/mdm.txt --output_dir /workspace/animation_from_TP/static/pose_video/skel/ --video_name skel"], shell=True, cwd=working_directory)
    #subprocess.run([f"python -m sample.double_take --model_path ./save/my_humanml_trans_enc_512/model000200000.pt --handshake_size 20 --blend_len 10 --input_text /workspace/animation_from_TP/mdm.txt --video_name {output_name}"], shell=True, cwd=working_directory)
    print("{} process is finished.".format(model))


def main():
    parser = argparse.ArgumentParser(description="prompt of action and background")
    parser.add_argument('--text_file', default='', type=str, help='path to a text file lists text prompts to be synthesized.')
    parser.add_argument('--text_prompt', default='', type=str, help = 'a text prompt to be generated.')

    args = parser.parse_args()

    texts = []
    if args.text_prompt != "":
        texts = [x + "." for x in re.split("[//.|//!|//?]", args.text_prompt) if x !=""]
    elif args.text_file != "":
        assert os.path.exists(args.text_file)
        with open(args.text_file, 'r') as f:
            texts = f.readlines()
        texts = [t.replace("\n", "")for t in texts]
        if '' in texts:
            texts.remove('')

    print(texts)

    action_list = []
    mdm_list = []
    condition_list = []
    #text_permission = input("Do you want to process the text (y/n): ")
    text_permission = True
    if text_permission:
        action_list, mdm_list, condition_list = text_process(texts)
        with open("./condition_list.txt", "w") as rf:
            print("in condition list: ", texts[0])
            rf.write(str(texts[0]) + '\n')
        with open("./mdm.txt", "w") as rf:
            for mdm in (mdm_list):
                rf.write(str(mdm) + '\n')
    else:
        print("Skip text processing...")

    #permission = input("Do you want to generate skeleton(y/n): ")
    permission = True
    if permission:
        action_name = "_".join(action_list)
        run_mdm("motion-diffusion-model", action_name)
    else:
        print("Skip generating skeleton...")

if __name__ == "__main__":
    main()

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


key_array = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
key_values_dict = {"C":0, "C#": 1, "Db": 1, "D": 2, "D#":3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb":6, "G":7, "G#":8, "Ab":8, "A": 9, "A#": 10, "Bb":10, "B":11}

url = input("Enter url of 91pu chords: ")
transpose_int = int(input("Enter semitones to transpose: "))


def transpose_chord(chord_text, dic):
    if (chord_text.find('#') == -1  and chord_text.find('b') == -1):
        return dic.get(chord_text[:1])+chord_text[1:]
    else:
        return dic.get(chord_text[:2])+chord_text[2:]

def get_transpose_dict(transpose):
    transpose_dict = {}
    for key in key_values_dict:
        idx = key_values_dict.get(key)
        transposed_idx = idx + transpose
        if transposed_idx > 11:
            transposed_idx = transposed_idx - 12
        transpose_dict[key] = key_array[transposed_idx]
    return transpose_dict
    
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

try:
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "lyric")) #wait 30 secs or wait till lyric element is out, whichever comes first
    )

    html = driver.page_source
    
    
    chord_list = driver.find_elements_by_class_name("tf")
    transpose_dict = get_transpose_dict(transpose_int)
    
    for chord in chord_list:    
        
        if (chord.text.find('/') == -1):
            transposed_chord = transpose_chord(chord.text, transpose_dict)
        else:
            arr = chord.text.split('/')
            transposed_chord = transpose_chord(arr[0], transpose_dict)+"/"+ transpose_chord(arr[1], transpose_dict)
        
        driver.execute_script("arguments[0].innerText = '"+transposed_chord+"'", chord)


finally:
    print("DONE!")
    # driver.quit()
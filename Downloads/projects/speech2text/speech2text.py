

def audio_analysis(audio_file):
    from matplotlib import pylab
    import numpy
    import scipy.io.wavfile
    samplerate, data = scipy.io.wavfile.read(audio_file)
    spectrum = numpy.fft.fft(data)
    frequencies = numpy.fft.fftfreq(len(spectrum))
    pylab.plot(frequencies,spectrum)
    pylab.show()

    
def convert2wav(filename,extn):
    from pydub import AudioSegment   
    flac_audio = AudioSegment.from_file(filename, format=extn)
    prefix = filename[:-4]
    flac_audio.export(prefix+".wav", format="wav")

    
def crop_audio(audio_file,start,end):
    from pydub import AudioSegment
    sound_file = AudioSegment.from_wav(audio_file)
    part_audio = sound_file[start:end]
    return part_audio

def audio_sampling(audio_file):
    audio=crop_audio(audio_file,3000,10000)
    audio.export("5sec.wav",format="wav")
    

def hp_filter(audio_file,freq=400,order=4):
   from pydub.scipy_effects import high_pass_filter as hpf
   from pydub import AudioSegment
   segfile = AudioSegment.from_wav(audio_file)
   outfile=hpf(segfile,freq,order)
   path="src_audio/filter.wav"
   outfile.export(path, format="wav")
   

def playback_change(path,audio_file,Change_RATE=2):
    import wave
    CHANNELS = 1
    swidth = 2
    spf = wave.open(path+"/"+audio_file, 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)
    newfile=path+"/"+audio_file[:-4]+'changed.wav'
    wf = wave.open(newfile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*Change_RATE)
    wf.writeframes(signal)
    wf.close()
    att(newfile)


def split_audio(audio_file,fdir):
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    sound_file = AudioSegment.from_wav(audio_file)
    audio_chunks = split_on_silence(sound_file, min_silence_len=100, silence_thresh=-50)
    for i, chunk in enumerate(audio_chunks):
        out_file = fdir+"/chunk"+str(i)+".wav"
        print ("exporting", out_file)
        chunk.export(out_file, format="wav")
#split_audio("amy.wav")


def iter_audio(audio_file):
    import os
    fdir="splits"
    split_audio(audio_file,fdir)
    for filename in os.listdir(fdir):
        if filename.endswith(".wav"):
            path=fdir+"/"+filename
            att(path)
            #os.remove(path)
#iter_audio("amy.wav")


def boost_audio(audio_file):
    from pydub import AudioSegment
    sound_file = AudioSegment.from_wav(audio_file)
    sound_boost=sound_file+20
    return sound_boost
    
    
def filter_silence(audio_file):
    from pydub import AudioSegment
    from pydub.utils import db_to_float
    sound_file = AudioSegment.from_wav(audio_file)
    average_loudness = sound_file.rms
    print(average_loudness)
    silence_threshold = average_loudness * db_to_float(-1)
    print(silence_threshold)
    # filter out the silence
    audio_chunks = (ms for ms in sound_file if ms.rms > silence_threshold)   
    return audio_chunks


def ats(audio_file):
    from pydub.playback import play
    from pydub import AudioSegment
    sound_file = AudioSegment.from_wav(audio_file)
    play(sound_file)
    
   
def sta(file):
    import speech_recognition as sr 
    r = sr.Recognizer()           
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    newfile="adaptation/"+file
    with open(newfile, "wb") as f:
        f.write(audio.get_wav_data())
    
        
def tts(txt):
#    from gtts import gTTS
#    blabla = (txt)
#    tts = gTTS(text=blabla, lang='en')
#    tts.save("d:/test.wav")
    import win32com.client as wincl
    speaker = wincl.Dispatch("SAPI.SpVoice")
    speaker.Speak(txt)
    
    
def tta(txt):
    from comtypes.client import CreateObject  
    engine = CreateObject("SAPI.SpVoice")
    stream = CreateObject("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib  
    outfile="splits/my_tta.wav"
    stream.Open(outfile, SpeechLib.SSFMCreateForWrite)
    engine.AudioOutputStream = stream
    #f = open(infile, 'r')
    #txt = f.read()
    #f.close()
    engine.speak(txt)
    stream.Close()


def txt_gen(audio):
    import speech_recognition as sr 
    r = sr.Recognizer()           
    try:
        txt=r.recognize_sphinx(audio)
        return txt 
    except sr.UnknownValueError: 
        return "error 104" 
    except sr.RequestError as e: 
        return e
    
        
def att(audio_file):
    import speech_recognition as sr 
    with sr.AudioFile(audio_file) as source:
        r = sr.Recognizer() 
        r.adjust_for_ambient_noise(source)
        audio = r.record(source) # read the entire audio file 
        txt=txt_gen(audio)
    return txt

                
def stt():
    import speech_recognition as sr           
    with sr.Microphone() as source:
        print("Listening...")
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        txt=txt_gen(audio)
    return txt
 

    
def file_read():
    infile="D:/Arun/pyprojects/research_projects/syntactics/gutenberg.txt"
    f = open(infile, 'r')
    txt = [line for line in f]
    f.close()
    i=0
    for line in txt:
        tts(line)
        if i==10:break 


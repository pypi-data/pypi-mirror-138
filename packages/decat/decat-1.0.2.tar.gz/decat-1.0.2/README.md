# Decat
```python
thisisawesome --> ['this', 'is', 'awesome']
```
---

[comment]: <> (badges 1)
<p align="center">
    <a href="#">
        <img src="https://forthebadge.com/images/badges/made-with-python.svg"/>
    </a>
    <a href="#">
        <img src="https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg"/>
    </a>
    <a href="#">
        <img src="https://forthebadge.com/images/badges/open-source.svg"/>
    </a>
    <a href="#">
        <img src="https://forthebadge.com/images/badges/built-with-love.svg"/>
    </a>
</p>

---

[comment]: <> (badges 2)
<p align="center">
    <a href="https://www.codefactor.io/repository/github/sudomode/decat">
        <img src="https://img.shields.io/codefactor/grade/github/sudomode/decat/master?style=for-the-badge"/>
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/v/release/sudomode/decat?style=for-the-badge"/>
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/languages/code-size/sudomode/decat?style=for-the-badge"/>
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/license/sudomode/decat?color=rgb%28100%2C%20150%2C%20150%29&style=for-the-badge"/>
    </a>
</p>

---


[comment]: <> (Into)
***Decat*** is a Python package capable of de-concatenating strings that do not have 
white-spaces in them, or in other words, it allows the user to infer spaces 
programmatically. This is a simple utility that comes in handy with various modern 
Natural Language Processing(NLP) tasks such as cleaning, exploration or even manipulation 
of text. [Zipf's Law](https://en.wikipedia.org/wiki/Zipf%27s_law) is 
at the 
core of this 
project, the aim is to provide an easy interface for programmers to extract meaningful 
information out of deformed pieces of texts.


## Get Started
> ### Install It
>>```python
>> >> pip install decat
>>```
> ### Play With It
>>```python
>> >> decat -i someweirdtext
>> >> ['some', 'weird', 'text']
>>```
>> or
>>```python
>> >> python -m decat -i justanotherstring
>> >> ['just', 'another', 'string']
>>```
> ### Use It In Your Projects
>> #### _Sample Code_
>>> ```python
>>> from decat import decat
>>> 
>>> 
>>> weird_text = '“AnyfoolcanwritecodethatacomputercanunderstandGoodprogrammerswritecodethathumanscanunderstand.”–MartinFowler'
>>> weird_text_simplified = decat(weird_text)
>>> print(weird_text_simplified)
>>>```
>> #### _Console_
>>> ['any', 'fool', 'can', 'write', 'code', 'that', 'a', 'computer', 'can', 
 'understand', 'good', 'programmers', 'write', 'code', 'that', 'humans', 'can', 
 'understand', 'martin', 'fowler'] 

## Features
>> 🪶 A light weight package, built around the features available in standard library
>
>> 📚 An ever-expanding vocabulary, knows more than 300K English words
> 
>> 🪃 Simplistic design, allows for easy expansion to new languages and custom vocabulary sets

## Dependencies
> ⭕️ ___None___ 🎉

## Limitations
> ❗ Requires Python >= 3.6
> 
> ❗ ️All input will be treated as lower-case
>>```python
>> >> ATitleCaseString --> ['a', 'title', 'case', 'string']
>>```
> ❗️ Punctuation marks, numbers and special characters will be stripped from the input and
> will not be preserved in the output
>>```python
>> >>  dummy.email1234@gmail.com --> ['dummy', 'email', 'gmail', 'com']
>>```
>

## Credits
>> [Generic Human](https://stackoverflow.com/users/1515832/generic-human)
> 
>> [Rachael Tatman](https://www.kaggle.com/rtatman)

## License
> ### MIT

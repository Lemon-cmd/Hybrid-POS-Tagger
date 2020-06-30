### **Hybrid Part of Speech Tagger**
---

**Objective**   
---

This part of speech tagger is built with the objective of utilizing stochastic methods and symbolic rules to tag a given input (sentence or sentences) that is either labeled or unlabeled.

---

**Background**
---    
   
This tagger is inspired by the Eric Brill's tagger developed in the late 90s and his machine learning technique ***transformation-based learning***.        
   
The difference between his tagger and this is the addition of continuous learning (only on supervised inputs), a limited lexicon, and linguistic rules such as suffix and prefix as well as symbolic rules derived from transistion with 100%. 

Lastly, it is still using the Brown corpus as its training sample.

---

**Status** 
---
The project is currently in ***development***

The overall goal of this project is to successfully tag labeled inputs with > 70% accuracy.

Current Accuracy = 55% 
   - Adding Rules for comparison between probabilities
   
---

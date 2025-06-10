# SMS Spam Classifier

This project documents the creation of a simple spam classifier to practice and understand the end-to-end workflow of a typical machine learning project. The model is built using Python, NLTK, and Scikit-learn.

**Note on the Dataset:** While the project is titled "SMS Spam Classifier," an email spam dataset was used for its accessibility and clear structure. The principles and techniques for text preprocessing, feature extraction, and classification are directly transferable to SMS data.

## Project Workflow

The process was broken down into five distinct steps, from acquiring data to evaluating the final model.

### 1. Data Collection

The project utilizes the [Spam or Not Spam Dataset from Kaggle](https://www.kaggle.com/datasets/ozlerhakan/spam-or-not-spam-dataset). This dataset consists of 3,000 text entries, each labeled as either not spam (`0`) or spam (`1`). The data was loaded into a Pandas DataFrame for manipulation.

```python
import pandas as pd
data = pd.read_csv('spam_or_not_spam.csv')
```

### 2. Data Preprocessing

To prepare the raw text for the model, a series of preprocessing steps were applied to each email. These steps are crucial for cleaning the data and reducing noise:

1.  **Tokenization:** Breaking down each string into a list of individual words (tokens).
2.  **Lowercasing:** Converting all characters to lowercase to treat words like "Free" and "free" as identical.
3.  **Stopword Removal:** Filtering out common words (e.g., 'the', 'a', 'in') that do not carry significant meaning for classification.
4.  **Stemming:** Reducing words to their root form (e.g., "congratulations" becomes "congratul") to group related words together.
5.  **Rejoining:** Reassembling the cleaned tokens back into a single string.

This was implemented in a single function and applied to the dataset.

```python
import nltk

nltk.download('stopwords')
nltk.download('punkt')

stop_words_set = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.snowball.SnowballStemmer('english')

def clean_and_word_tokenize(string):
    if not isinstance(string, str):
        return ''
    
    string = nltk.tokenize.word_tokenize(string) # tokenization
    string = [i.lower() for i in string] # lower all of the tokens
    string = [i for i in string if i not in stop_words_set] # removing the words that are stop word
    string = [stemmer.stem(i) for i in string] # stemming
    string = ' '.join(string) # joining the words list to a singular string
    return string

data.iloc[:, 0] = data.iloc[:, 0].apply(clean_and_word_tokenize)
```

### 3. Feature Extraction

Machine learning models require numerical input. The preprocessed text data was transformed into a numerical format using the **Bag-of-Words (BoW)** technique. Scikit-learn's `CountVectorizer` was used to create a matrix of token counts, representing the frequency of each word in each document.

```python
import sklearn

vectorizer = sklearn.feature_extraction.text.CountVectorizer()
X = vectorizer.fit_transform(data.iloc[:, 0])
y = data.iloc[:, 1]
```

### 4. Model Training

The dataset was split into an 80% training set and a 20% testing set.

For the classification task, a **Multinomial Naive Bayes (MultinomialNB)** model was chosen. As I learned during my research, this algorithm is statistically efficient and performs very well on text classification tasks that involve word counts, making it a strong choice for spam detection.

```python
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=0)

classifier_model = sklearn.naive_bayes.MultinomialNB()
classifier_model.fit(X_train, y_train)
```

### 5. Model Evaluation

The model's performance was measured using two methods: a quantitative accuracy score on the test set and a qualitative review with custom inputs.

#### **Quantitative Results**

The model was evaluated against the 20% test set that it had not seen during training.

```python
score = classifier_model.score(X_test, y_test)
print(f"The accuracy of the model on the splitted test: {score:.1%}")
```

**Result:**
> *The accuracy of the model on the splitted test: 99.3%*

#### **Qualitative Manual Testing**

To better understand the model's real-world behavior, I tested it with several custom sentences.

```python
def testing_model(string_input):
    string_input = clean_and_word_tokenize(string_input)
    string_input = vectorizer.transform([string_input])
    prediction = classifier_model.predict(string_input)
    return prediction

test_inputs = [
    'Hey, are we still meeting at 3pm?',
    'Congratulations, you have won a free iPhone!',
    'Can you send the report by tomorrow?',
    'URGENT! Claim your $1000 gift card now!',
    'Let’s grab lunch this week.',
    'You’ve been selected for a limited-time offer!',
    'Don’t forget the team call at 10am.',
    'Act now to get 50% off!',
    'Just checking in—how’s everything going?',
    'This isn’t spam. I really need your help with something.'
]

for test_input in test_inputs:
    prediction = testing_model(test_input)
    print(f"Input: {test_input}\nPrediction: {'Spam' if prediction[0] == 1 else 'Not Spam'}\n")
```

**Results from Manual Tests:**
```
Input: Hey, are we still meeting at 3pm?
Prediction: Not Spam

Input: Congratulations, you have won a free iPhone!
Prediction: Spam

Input: Can you send the report by tomorrow?
Prediction: Spam

Input: URGENT! Claim your $1000 gift card now!
Prediction: Spam

Input: Let’s grab lunch this week.
Prediction: Not Spam

Input: You’ve been selected for a limited-time offer!
Prediction: Not Spam

Input: Don’t forget the team call at 10am.
Prediction: Not Spam

Input: Act now to get 50% off!
Prediction: Not Spam

Input: Just checking in—how’s everything going?
Prediction: Not Spam

Input: This isn’t spam. I really need your help with something.
Prediction: Not Spam
```

#### **Analysis of Results**

The model achieved a very high accuracy of 99.3% on the test data. The manual tests reveal more nuance:
*   The model is effective at identifying clear-cut spam ("free iPhone", "URGENT! Claim") and legitimate messages ("meeting at 3pm").
*   **Interesting Misclassifications:** The model flagged a neutral business message (`Can you send the report by tomorrow?`) as **Spam**. This might indicate that the word "report" appears frequently in the spam section of the training data (e.g., "credit report").
*   Conversely, it classified common marketing phrases (`limited-time offer`, `50% off`) as **Not Spam**. This suggests the model's understanding of spam is heavily biased towards the specific types of spam present in the training dataset and may not generalize perfectly to modern marketing language.

## Conclusion and Future Work

This project was a successful exercise in applying the machine learning workflow. The Multinomial Naive Bayes model proved to be a powerful and effective baseline for text classification. The evaluation highlighted the importance of not only relying on accuracy scores but also performing qualitative analysis to understand a model's strengths and weaknesses.

Based on this project, my future learning goals are to:
1.  **Explore Alternative Models:** Compare the performance of this Naive Bayes model with other algorithms like Support Vector Machines (SVM) and Logistic Regression.
2.  **Advance Feature Engineering:** Implement more sophisticated techniques like TF-IDF (Term Frequency-Inverse Document Frequency) to see if it improves the model's ability to identify nuanced spam.
3.  **Build and Deploy:** Take a future project to the final step by creating an interactive web-based GUI (using Flask or Streamlit) so that it can be used by others.
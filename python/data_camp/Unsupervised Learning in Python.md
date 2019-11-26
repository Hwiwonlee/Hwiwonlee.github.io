# 1. Clustering for dataset exploration
## 1.1 Unsupervised Learning

```python
# Clustering 2D points
## Import KMeans
from sklearn.cluster import KMeans

model = KMeans(n_clusters = 3) ## Create a KMeans instance with 3 clusters: model
model.fit(points) ## Fit model to points
labels = model.predict(new_points) ## Determine the cluster labels of new_points: labels

## Print cluster labels of new_points
print(labels)
```

```python
# Inspect your clustering
import matplotlib.pyplot as plt

## Assign the columns of new_points: xs and ys
xs = new_points[:, 0]
ys = new_points[:, 1]

## Make a scatter plot of xs and ys, using labels to define the colors
plt.scatter(xs, ys, c=labels, alpha=0.5)

## Assign the cluster centers: centroids
centroids = model.cluster_centers_

## Assign the columns of centroids: centroids_x, centroids_y
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]

## Make a scatter plot of centroids_x and centroids_y
plt.scatter(centroids_x, centroids_y, marker='D', s=50)
plt.show()

```

## 1.2 Evaluating a clustering

```python
# How many clusters of grain?
## Using seed dataset
ks = range(1, 6)
inertias = []

for k in ks:
    ## Create a KMeans instance with k clusters: model
    model = KMeans(n_clusters=k)
    
    ## Fit model to samples
    model.fit(samples)
    
    ## Append the inertia to the list of inertias
    inertias.append(model.inertia_)
    
## Plot ks vs inertias
plt.plot(ks, inertias, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()
```
> TO do. .append() 사용법이 헷갈린다. 복습하기


```python
# Evaluating the grain clustering
model = KMeans(3) ## Create a KMeans model with 3 clusters: model

labels = model.fit_predict(samples) ## Use fit_predict to fit model and obtain cluster labels: labels

## Create a DataFrame with labels and varieties as columns: df
df = pd.DataFrame({'labels': labels, 'varieties': varieties})

## Create crosstab: ct
ct = pd.crosstab(df['labels'], df['varieties'])
print(ct) ## Display ct
```
> pd.crosstab() : Frequency Table를 만드는 함수

## 1.3 Transforming features for better clusterings

```python
# Scaling fish data for clustering
## Perform the necessary imports
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

scaler = StandardScaler() ## Create scaler: scaler
kmeans = KMeans(4) ## Create KMeans instance: kmeans

pipeline = make_pipeline(scaler, kmeans) ## Create pipeline: pipeline
```

```python
# Clustering the fish data
import pandas as pd

pipeline.fit(samples) ## Fit the pipeline to samples
labels = pipeline.predict(samples) ## Calculate the cluster labels: labels

## Create a DataFrame with labels and species as columns: df
df = pd.DataFrame({'labels':labels, 'species':species})

## Create crosstab: ct
ct = pd.crosstab(df['labels'], df['species'])
print(ct)
```

```python
# Clustering stocks using KMeans
## Using movements array
from sklearn.preprocessing import Normalizer ## Import Normalizer

normalizer = Normalizer() ## Create a normalizer: normalizer
kmeans = KMeans(10) ## Create a KMeans model with 10 clusters: kmeans

## Make a pipeline chaining normalizer and kmeans: pipeline
pipeline = make_pipeline(normalizer, kmeans)

## Fit pipeline to the daily price movements
pipeline.fit(movements)
```

```python
# Which stocks move together?
import pandas as pd

## Predict the cluster labels: labels
labels = pipeline.predict(movements)

## Create a DataFrame aligning labels and companies: df
df = pd.DataFrame({'labels': labels, 'companies': companies})

print(df.sort_values('labels')) ## Display df sorted by cluster label
```
# 2. Visualization with hierarchical clustering and t-SNE
## 2.1 Visualizing hierarchies


```python
# Hierarchical clustering of the grain data
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

mergings = linkage(samples, method='complete') ## Calculate the linkage: mergings

## Plot the dendrogram, using varieties as labels
dendrogram(mergings,
           labels=varieties,
           leaf_rotation=90,
           leaf_font_size=6,
)
plt.show()

```

```python
# Hierarchies of stocks
from sklearn.preprocessing import normalize

## Normalize the movements: normalized_movements
normalized_movements = normalize(movements)

## Calculate the linkage: mergings
mergings = linkage(normalized_movements, method='complete')

## Plot the dendrogram
dendrogram(mergings, 
           labels=companies,
           leaf_rotation = 90,
           leaf_font_size = 6)
plt.show()
```

## 2.2 Cluster labels in hierarchical clustering


```python
# Different linkage, different hierarchical clustering!
## Using https://eurovision.tv/history/full-split-results
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

## Calculate the linkage: mergings
mergings = linkage(samples, method='single')

## Plot the dendrogram
dendrogram(mergings, 
           labels=country_names, 
           leaf_rotation = 90,
           leaf_font_size = 6)
plt.show()
```

```python
# Extracting the cluster labels
import pandas as pd
from scipy.cluster.hierarchy import fcluster

## Use fcluster to extract labels: labels
labels = fcluster(mergings, 6, criterion='distance')

## Create a DataFrame with labels and varieties as columns: df
df = pd.DataFrame({'labels': labels, 'varieties': varieties})

## Create crosstab: ct
ct = pd.crosstab(df['labels'], df['varieties'])

## Display ct
print(ct)
```

## 2.3 t-SNE for 2-dimensional maps

```python
# t-SNE visualization of grain dataset
from sklearn.manifold import TSNE

model = TSNE(learning_rate=200) ## Create a TSNE instance: model
tsne_features = model.fit_transform(samples) ## Apply fit_transform to samples: tsne_features

xs = tsne_features[:,0] ## Select the 0th feature: xs
ys = tsne_features[:,1] ## Select the 1st feature: ys

# Scatter plot, coloring by variety_numbers
plt.scatter(xs, ys, c=variety_numbers)
plt.show()
```

```python
# A t-SNE map of the stock market
from sklearn.manifold import TSNE

model = TSNE(learning_rate=50) ## Create a TSNE instance: model

## Apply fit_transform to normalized_movements: tsne_features
tsne_features = model.fit_transform(normalized_movements)

xs = tsne_features[:, 0] ## Select the 0th feature: xs
ys = tsne_features[:,1] ## Select the 1th feature: ys

plt.scatter(xs, ys, alpha = 0.5) ## Scatter plot

## Annotate the points
for x, y, company in zip(xs, ys, companies):
    plt.annotate(company, (x, y), fontsize=5, alpha=0.75)
plt.show()
```

# 3. Decorrelating your data and dimension reduction
## 3.1 Visualizing the PCA transformation

```python
# Correlated data in nature
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

width = grains[:, 0] ## Assign the 0th column of grains: width
length = grains[:, 1] ## Assign the 1st column of grains: length

## Scatter plot width vs length
plt.scatter(width, length)
plt.axis('equal')
plt.show()

correlation, pvalue = pearsonr(width, length) ## Calculate the Pearson correlation
print(correlation)
```

```python
# Decorrelating the grain measurements with PCA
from sklearn.decomposition import PCA

model = PCA() ## Create PCA instance: model
pca_features = model.fit_transform(grains) ## Apply the fit_transform method of model to grains: pca_features

xs = pca_features[:,0] ## Assign 0th column of pca_features: xs
ys = pca_features[:,1] ## Assign 1st column of pca_features: ys

plt.scatter(xs, ys)
plt.axis('equal')
plt.show()

correlation, pvalue = pearsonr(xs, ys) ## Calculate the Pearson correlation of xs and ys
print(correlation)
```

## 3.2 Intrinsic dimension

```python
# The first principal component
plt.scatter(grains[:,0], grains[:,1]) ## Make a scatter plot of the untransformed points

model = PCA() ## Create a PCA instance: model
model.fit(grains) ## Fit model to points

mean = model.mean_ ## Get the mean of the grain samples: mean

first_pc = model.components_[0, :] ## Get the first principal component: first_pc

## Plot first_pc as an arrow, starting at mean
plt.arrow(mean[0], mean[1], first_pc[0], first_pc[1], color='red', width=0.01)

## Keep axes on same scale
plt.axis('equal')
plt.show()
```

```python
# Variance of the PCA features
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt

scaler = StandardScaler() ## Create scaler: scaler
pca = PCA() ## Create a PCA instance: pca

## Create pipeline: pipeline
pipeline = make_pipeline(scaler, pca)

## Fit the pipeline to 'samples'
pipeline.fit(samples)

## Plot the explained variances
features = range(pca.n_components_)
plt.bar(features, pca.explained_variance_)
plt.xlabel('PCA feature')
plt.ylabel('variance')
plt.xticks(features)
plt.show()
```
## 3.3 Dimension reduction with PCA

```python
# Dimension reduction of the fish measurements
from sklearn.decomposition import PCA

## Create a PCA model with 2 components: pca
pca = PCA(n_components=2)

## Fit the PCA instance to the scaled samples
pca.fit(scaled_samples)

## Transform the scaled samples: pca_features
pca_features = pca.transform(scaled_samples)

## Print the shape of pca_features
print(pca_features.shape)
```

```python
# A tf-idf word-frequency array
## Import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()  ## Create a TfidfVectorizer: tfidf

csr_mat = tfidf.fit_transform(documents) ## Apply fit_transform to document: csr_mat
print(csr_mat.toarray()) ## Print result of toarray() method

words = tfidf.get_feature_names() ## Get the words: words
print(words)
```

```python
# Clustering Wikipedia part I
## Perform the necessary imports
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

svd = TruncatedSVD(n_components=50) ## Create a TruncatedSVD instance: svd
kmeans = KMeans(n_clusters=6) ## Create a KMeans instance: kmeans

pipeline = make_pipeline(svd, kmeans) ## Create a pipeline: pipeline
```

```python
# Clustering Wikipedia part II
import pandas as pd

pipeline.fit(articles) ## Fit the pipeline to articles
labels = pipeline.predict(articles) ## Calculate the cluster labels: labels

## Create a DataFrame aligning labels and titles: df
df = pd.DataFrame({'label': labels, 'article': titles})
print(df.sort_values('label')) ## Display df sorted by cluster label
```

# 4. Discovering interpretable features
## 4.1 Non-negative matrix factorization (NMF)

```python
# NMF applied to Wikipedia articles
from sklearn.decomposition import NMF ## Import NMF

model = NMF(6) ## Create an NMF instance: model
model.fit(articles) ## Fit the model to articles

## Transform the articles: nmf_features
nmf_features = model.transform(articles)
print(nmf_features)

```

```python
# NMF features of the Wikipedia articles
import pandas as pd ## Import pandas

## Create a pandas DataFrame: df
df = pd.DataFrame(nmf_features, index=titles)

## Print the row for 'Anne Hathaway'
print(df.loc['Anne Hathaway'])

## Print the row for 'Denzel Washington'
print(df.loc['Denzel Washington'])

```
## 4.2 NMF learns interpretable parts

```python
# NMF learns topics of documents
import pandas as pd

## Create a DataFrame: components_df
components_df = pd.DataFrame(model.components_, columns=words)
print(components_df.shape) ## Print the shape of the DataFrame

component = components_df.iloc[3] ## Select row 3: component
print(component.nlargest())
```

```python
# Explore the LED digits dataset
from matplotlib import pyplot as plt

digit = samples[0, :] ## Select the 0th row: digit
print(digit) ## Print digit

## Reshape digit to a 13x8 array: bitmap
bitmap = digit.reshape(13, 8) 
print(bitmap) ## Print bitmap

## Use plt.imshow to display bitmap
plt.imshow(bitmap, cmap='gray', interpolation='nearest')
plt.colorbar()
plt.show()
```

```python
# NMF learns the parts of images
from sklearn.decomposition import NMF

model = NMF(7) ## Create an NMF model: model
features = model.fit_transform(samples) ## Apply fit_transform to samples: features

## Call show_as_image on each component
for component in model.components_:
    show_as_image(component)

## Assign the 0th row of features: digit_features
digit_features = features[0, :]
print(digit_features)
```

```python
# PCA doesn't learn parts
from sklearn.decomposition import PCA

model = PCA(7) ## Create a PCA instance: model
features = model.fit_transform(samples) ## Apply fit_transform to samples: features

## Call show_as_image on each component
for component in model.components_:
    show_as_image(component)
```

## 4.3 Building recommender systems using NMF

```python
# Which articles are similar to 'Cristiano Ronaldo'?
## Perform the necessary imports
import pandas as pd
from sklearn.preprocessing import normalize

norm_features = normalize(nmf_features) ## Normalize the NMF features: norm_features

df = pd.DataFrame(norm_features, index = titles) ## Create a DataFrame: df
article = df.loc['Cristiano Ronaldo', :] ## Select the row corresponding to 'Cristiano Ronaldo': article
similarities = df.dot(article) ## Compute the dot products: similarities

print(similarities.nlargest()) ## Display those with the largest cosine similarity
```

> To do. 메시로 바꿀 것 

```python
# Recommend musical artists part I
## Perform the necessary imports
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer, MaxAbsScaler
from sklearn.pipeline import make_pipeline

scaler = MaxAbsScaler() ## Create a MaxAbsScaler: scaler
nmf = NMF(20) ## Create an NMF model: nmf
normalizer = Normalizer() ## Create a Normalizer: normalizer

pipeline = make_pipeline(scaler, nmf, normalizer) ## Create a pipeline: pipeline

## Apply fit_transform to artists: norm_features
norm_features = pipeline.fit_transform(artists)
```

```python
# Recommend musical artists part II
import pandas as pd

df = pd.DataFrame(norm_features, index=artist_names) ## Create a DataFrame: df

artist = df.loc['Bruce Springsteen', : ] ## Select row of 'Bruce Springsteen': artist 
similarities = df.dot(artist) ## Compute cosine similarities: similarities

## Display those with highest cosine similarity
print(similarities.nlargest())
```

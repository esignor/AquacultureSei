from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import community  # modulo per Louvain clustering (da installare con: pip install python-louvain)
import networkx as nx
import numpy as np

# 1. Carica la matrice binaria X (forma: n_windows x n_profili)
# Ogni riga rappresenta una finestra genomica, ogni colonna un profilo binario (presenza/assenza).
# Per dlabarx2021: (239064 windows, 103 profili)
X = np.load("binary_overlaps_dlabrax2021.npy")

# 2. Riduzione dimensionale con PCA
# Applica PCA per ridurre la dimensionalità da 103 a 50 componenti principali (nel paper SEI)  e' 180, noi abbiamo solo 103 profili inoltre si devono riassumere solo 3 classi di sequenza).
# Serve a ridurre il rumore e rendere i dati più gestibili per il clustering
pca = PCA(n_components=50)
X_pca = pca.fit_transform(X)  # Matrice trasformata: (n_windows, 50)

# 3. Costruzione del grafo k-NN (k-nearest neighbors)
# Si collega ogni punto ai suoi 14 vicini più vicini (da paper SEI) in base alla distanza euclidea nello spazio PCA.
k = 14
nn = NearestNeighbors(n_neighbors=k)
nn.fit(X_pca)  # Costruisce la struttura per la ricerca dei vicini sui 50 profili sottodimensionati
distances, indices = nn.kneighbors(X_pca)  # Trova per ogni punto i suoi k vicini (si costruisce una prima struttura che riassuma utilizzando le finestre i profili di cromatina nelle classi di sequenza)

# 4. Costruzione del grafo non orientato da usare per Louvain
# Ogni nodo rappresenta una finestra. Gli archi collegano i nodi ai loro vicini k-NN.
edges = []
for i, neighbors in enumerate(indices):
    for j in neighbors:
        if i != j:  # evita self-loops
            edges.append((i, j))  # aggiunge arco da i a j

G = nx.Graph()
G.add_edges_from(edges)  # costruisce il grafo completo

# 5. Clustering con Louvain
# Louvain è un algoritmo di clustering che rileva comunità in grafi in modo efficiente
# Ritorna un dizionario: {nodo: cluster_id}, in questo modo si cerca di clusterizzare le windows per qualche tema (e fare cosi un abazzo grezzo delle classi di sequenza)
partition = community.best_partition(G)

# Converte il dizionario in un array numpy di etichette cluster (una per ogni finestra)
labels = np.array([partition[i] for i in range(len(X))])

# 6. Costruzione della matrice projvec_targets (inizializzazione della struttura)
# Per ogni cluster identificato, crea un "profilo aggregato" binario.
# L'output è una matrice (n_cluster x n_profili), dove ogni riga rappresenta; i cluster rappresentano le classi di sequenza
# un profilo aggregato binario che indica se almeno una finestra del cluster ha 1 in quella colonna.
n_clusters = labels.max() + 1 # numero totale di cluster trovati con Louvain
projvec_targets = np.zeros((n_clusters, X.shape[1]), dtype=np.float32) # inizializza una matrice vuota per contenere i profili aggregati

# Per ogni cluster, somma i profili delle finestre e metti 1 se c'è almeno un 1 (cioè 'OR' logico)
for class_id in range(n_clusters):
    members = X[labels == class_id]  # seleziona tutte le finestre che appartengono al cluster class_id
    projvec_targets[class_id] = members.mean(axis=0)  # profilo aggregato (somma i profili riga per riga (quindi somma colonna per colonna)). 
    # Se in una colonna c'è almeno un 1 (profilo e' attivo) si diviede per il numero totale di finestre nel cluster


# 7. Salvataggio del risultato finale
# Salva la matrice dei profili aggregati su file (formato .npy) con shape (n_cluster NON PREDEFINITO DIPENDE DA LOUVAIN)x(chromatine profiles)
np.save("projvec_targets_dlabrax2021.npy", projvec_targets)

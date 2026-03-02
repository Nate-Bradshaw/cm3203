# ================================================================================================
# Initalize midisim
# ================================================================================================

# Import main midisim module
import midisim

# ================================================================================================
# Prepare midisim embeddings
# ================================================================================================

# Option 1: Download sample pre-computed embeddings corpus from Hugging Face
# emb_path = midisim.download_embeddings()

# Option 2: use custom pre-computed embeddings corpus
# See custom embeddings generation section of this README for details
emb_path = './midisim-embeddings\discover_midi_dataset_37292_genres_midis_embeddings_cc_by_nc_sa.npy'

# Load downloaded embeddings corpus
corpus_midi_names, corpus_emb = midisim.load_embeddings(emb_path)

# ================================================================================================
# Prepare midisim model
# ================================================================================================

# Option 1: Download main pre-trained midisim model from Hugging Face
#model_path = midisim.download_model()

# Option 2: Use main pre-trained midisim model included in midisim PyPI package
#model_path = midisim.get_package_models()[0]['path']
model_path = './midisim-models/midisim_small_pre_trained_model_2_epochs_43117_steps_0.3148_loss_0.9229_acc.pth'

# Load midisim model
model, ctx, dtype = midisim.load_model(model_path)

# ================================================================================================
# Prepare source MIDI
# ================================================================================================

# Load source MIDI
input_toks_seqs = midisim.midi_to_tokens('Untitled_31_short.mid')

# ================================================================================================
# Calculate and analyze embeddings
# ================================================================================================

# Compute source/query embeddings
query_emb = midisim.get_embeddings_bf16(model, input_toks_seqs)
#! above should be all we need to compare generated midi to the original for simularity

# Calculate cosine similarity between source/query MIDI embeddings and embeddings corpus
idxs, sims = midisim.cosine_similarity_topk(query_emb, corpus_emb)

# ================================================================================================
# Processs, print and save results
# ================================================================================================

# Convert the results to sorted list with transpose values
idxs_sims_tvs_list = midisim.idxs_sims_to_sorted_list(idxs, sims)

# Print corpus matches (and optionally) convert the final result to a handy list for further processing
corpus_matches_list = midisim.print_sorted_idxs_sims_list(idxs_sims_tvs_list, corpus_midi_names, return_as_list=True)

# ================================================================================================
# Copy matched MIDIs from the MIDI corpus for listening and further evaluation and analysis
# ================================================================================================

# Copy matched corpus MIDI to a desired directory for easy evaluation and analysis
out_dir_path = midisim.copy_corpus_files(corpus_matches_list)

# ================================================================================================

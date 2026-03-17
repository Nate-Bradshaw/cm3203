import midisim

midismVerbose = False

#pre downloaded embedding and model
emb_path = './midisim-embeddings\discover_midi_dataset_37292_genres_midis_embeddings_cc_by_nc_sa.npy'
model_path = './midisim-models/midisim_small_pre_trained_model_2_epochs_43117_steps_0.3148_loss_0.9229_acc.pth'
midi_path_rel0 = 'Untitled_31_short.mid'
midi_path_rel1 = 'Untitled_15.mid'

#embedings
corpus_midi_names, corpus_emb = midisim.load_embeddings(emb_path, verbose=midismVerbose)

#midisim model
model, ctx, dtype = midisim.load_model(model_path, verbose=midismVerbose)

def getEmbeddingFile(path):
    input_toks_seqs = midisim.midi_to_tokens(path, verbose=midismVerbose)
    return midisim.get_embeddings_bf16(model, input_toks_seqs, verbose=midismVerbose)

#MIDI data in a buffer
def getEmbeddingBuf(buf):
    input_toks_seqs = midisim.midi_to_tokens(buf, verbose=midismVerbose)
    return midisim.get_embeddings_bf16(model, input_toks_seqs, verbose=midismVerbose)

def compareEmbeddings(emb1, emb2):
    #comparing emb2's simularity to emb1
    best_idx, best_vals = midisim.cosine_similarity_topk(emb1, emb2, verbose=midismVerbose)
    similarity_score = best_vals[0][0]  # scalar float
    print(f"Similarity: {similarity_score:.4f}")

"""
score = 1: exact match
score > 0.85: very similar
score > 0.6: moderately similar
score > 0.3: loosely similar
otherwise dissimilar
"""
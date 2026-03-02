# Import main midisim module
import midisim

# ================================================================================================
# Prepare midisim embeddings
# ================================================================================================

#pre downloaded embedding and model
emb_path = './midisim-embeddings\discover_midi_dataset_37292_genres_midis_embeddings_cc_by_nc_sa.npy'
model_path = './midisim-models/midisim_small_pre_trained_model_2_epochs_43117_steps_0.3148_loss_0.9229_acc.pth'
midi_path_rel0 = 'Untitled_31_short.mid'
midi_path_rel1 = 'Untitled_15.mid'

#embedings
corpus_midi_names, corpus_emb = midisim.load_embeddings(emb_path)

#midisim model
model, ctx, dtype = midisim.load_model(model_path)

#input midi 0
input_toks_seqs0 = midisim.midi_to_tokens(midi_path_rel0)

query_emb0 = midisim.get_embeddings_bf16(model, input_toks_seqs0)

#input midi 1
input_toks_seqs1 = midisim.midi_to_tokens(midi_path_rel1)

query_emb1 = midisim.get_embeddings_bf16(model, input_toks_seqs1)

"""
best_idx, best_vals = midisim.cosine_similarity_topk(query_emb, corpus_emb)

similarity_score = best_vals[0][0]  # scalar float

print(f"Similarity: {similarity_score:.4f}")

if similarity_score > 0.85:
    print("Very similar")
elif similarity_score > 0.6:
    print("Moderately similar")
elif similarity_score > 0.3:
    print("Loosely related")
else:
    print("Dissimilar")
"""
    
best_idx, best_vals = midisim.cosine_similarity_topk(query_emb0, query_emb1)

similarity_score = best_vals[0][0]  # scalar float

print(f"Similarity: {similarity_score:.4f}")

if similarity_score > 0.85:
    print("Very similar")
elif similarity_score > 0.6:
    print("Moderately similar")
elif similarity_score > 0.3:
    print("Loosely related")
else:
    print("Dissimilar")


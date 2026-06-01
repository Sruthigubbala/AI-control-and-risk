import torch.nn as nn
from transformers import AutoModel

class LegalClauseClassifier(nn.Module):
    def __init__(self, model_name="bert-base-uncased", num_classes=2):
        super().__init__()

        self.bert = AutoModel.from_pretrained(model_name)

        self.fc = nn.Linear(
            self.bert.config.hidden_size,
            num_classes
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled = outputs.last_hidden_state[:, 0]

        return self.fc(pooled)
import torch
from torch import nn

class TMDLayer(nn.Module):
    def __init__(
        self,
        in_features = 28*28,
        L_latent = 16,
        epsilon = 0.25
    ):
        super().__init__()
        

        self.pi = nn.Sequential(nn.Linear(L_latent, in_features), 
                                                    nn.ReLU(),
                                                    nn.Linear(in_features, 1),
                                                    nn.Sigmoid())
        self.dt = nn.Parameter(torch.FloatTensor([0.1]))

        self.epsilon = epsilon
        self.proj = nn.Sequential(nn.Linear(in_features, L_latent))
    

    def TMD_map(self, x):
        # input x if of size [B, N, d]
        x = self.proj(x)
        # L = construct from pe

        i_minus_j = x.unsqueeze(2) - x.unsqueeze(1)
        K_epsilon = torch.exp(-1 / (4 * self.epsilon) * (i_minus_j ** 2).sum(dim=3))

        ### construct TMD
        q_epsilon_tilde = K_epsilon.sum(dim=2)
        D_epsilon_tilde = torch.diag_embed(self.pi(x).squeeze(2) / q_epsilon_tilde)
        K_tilde = K_epsilon.bmm(D_epsilon_tilde)
        D_tilde = torch.diag_embed(K_tilde.sum(dim=2) +
                                   1e-5 * torch.ones(K_tilde.shape[0], K_tilde.shape[1]).to(x.device))
        L = 1 / self.epsilon * (torch.inverse(D_tilde).bmm(K_tilde)) - torch.eye(K_tilde.shape[1]).to(
            x.device).unsqueeze(0).repeat(x.shape[0], 1, 1)
        return L

        
    def forward(self, x):
        L = self.TMD_map(x)

        x = (x + self.dt*torch.matmul(L, x))

        return x
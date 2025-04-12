import torch
import torch.nn as nn

# Channel Attention
class ChannelAttention(nn.Module):
    def __init__(self, in_planes, ratio=8):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        self.shared_mlp = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // ratio, 1),
            nn.ReLU(),
            nn.Conv2d(in_planes // ratio, in_planes, 1)
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.shared_mlp(self.avg_pool(x))
        max_out = self.shared_mlp(self.max_pool(x))
        return self.sigmoid(avg_out + max_out)

# Spatial Attention
class SpatialAttention(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Conv2d(2, 1, kernel_size=7, padding=3)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x_cat = torch.cat([avg_out, max_out], dim=1)
        return self.sigmoid(self.conv(x_cat))

# CBAM Module (Channel + Spatial Attention)
class CBAM(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.channel_attention = ChannelAttention(channels)
        self.spatial_attention = SpatialAttention()

    def forward(self, x):
        x = x * self.channel_attention(x)
        return x * self.spatial_attention(x)

# Final Generator Model (U-Net + CBAM + Multimodal)
class UNetGeneratorCBAM_Multimodal(nn.Module):
    def __init__(self):
        super().__init__()
        self.down1 = self.block(2, 64, batch_norm=False)  # input: grayscale + noise
        self.cbam1 = CBAM(64)

        self.down2 = self.block(64, 128)
        self.cbam2 = CBAM(128)

        self.down3 = self.block(128, 256)
        self.cbam3 = CBAM(256)

        self.down4 = self.block(256, 512)
        self.cbam4 = CBAM(512)

        self.bottleneck = nn.Sequential(
            nn.Conv2d(512, 1024, 4, 2, 1),
            nn.ReLU()
        )

        self.up1 = self.up_block(1024, 512)
        self.up2 = self.up_block(1024, 256)
        self.up3 = self.up_block(512, 128)
        self.up4 = self.up_block(256, 64)

        self.final = nn.Sequential(
            nn.ConvTranspose2d(128, 3, 4, 2, 1),
            nn.Tanh()
        )

    def block(self, in_c, out_c, batch_norm=True):
        layers = [nn.Conv2d(in_c, out_c, 4, 2, 1), nn.LeakyReLU(0.2)]
        if batch_norm:
            layers.append(nn.BatchNorm2d(out_c))
        return nn.Sequential(*layers)

    def up_block(self, in_c, out_c):
        return nn.Sequential(
            nn.ConvTranspose2d(in_c, out_c, 4, 2, 1),
            nn.ReLU(),
            nn.BatchNorm2d(out_c)
        )

    def forward(self, x, z):
        x = torch.cat([x, z], dim=1)  # concat grayscale and noise
        d1 = self.cbam1(self.down1(x))
        d2 = self.cbam2(self.down2(d1))
        d3 = self.cbam3(self.down3(d2))
        d4 = self.cbam4(self.down4(d3))

        bn = self.bottleneck(d4)

        u1 = self.up1(bn)
        u1 = torch.cat([u1, d4], dim=1)

        u2 = self.up2(u1)
        u2 = torch.cat([u2, d3], dim=1)

        u3 = self.up3(u2)
        u3 = torch.cat([u3, d2], dim=1)

        u4 = self.up4(u3)
        u4 = torch.cat([u4, d1], dim=1)

        return self.final(u4)

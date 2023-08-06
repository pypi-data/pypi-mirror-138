import math

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.modules.module import Module


def print_gcn():
    print(
        """
class GraphConvolution(Module):
    # Simple GCN layer, similar to https://arxiv.org/abs/1609.02907

    def __init__(self, in_features, out_features, bias=True):
        super(GraphConvolution, self).__init__()
        # 初始化变量
        self.in_features = in_features
        self.out_features = out_features
        self.weight = Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = Parameter(torch.FloatTensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        # self.weight.size(1)返回的是weight.size()中的第1个元素(从0开始)
        # 也就是返回了out_features
        stdv = 1. / math.sqrt(self.weight.size(1))
        # 从(-stdv, stdv)均匀分布中初始化权重
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input, adj):
        # 矩阵乘法(input x self.weight)
        support = torch.mm(input, self.weight)
        # 稀疏矩阵乘法
        output = torch.spmm(adj, support)
        if self.bias is not None:
            return output + self.bias
        else:
            return output

    def __repr__(self):
        return self.__class__.__name__ + ' (' \
               + str(self.in_features) + ' -> ' \
               + str(self.out_features) + ')'


class GCN(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout):
        super(GCN, self).__init__()

        self.gc1 = GraphConvolution(nfeat, nhid)
        self.gc2 = GraphConvolution(nhid, nclass)
        self.dropout = dropout

    def forward(self, x, adj):
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        x = self.gc2(x, adj)
        return F.log_softmax(x, dim=1)

        """
    )


def print_sgc():
    print(
        """
        class SGC(nn.Module):
    
    # A Simple PyTorch Implementation of Logistic Regression.
    # Assuming the features have been preprocessed with k-step graph propagation.
    
    def __init__(self, nfeat, nclass):
        super(SGC, self).__init__()

        self.W = nn.Linear(nfeat, nclass)

    def forward(self, x):
        return self.W(x)
        """
    )


def print_gat():
    print(       
"""
class GraphAttentionLayer(nn.Module):
    #Simple GAT layer, similar to https://arxiv.org/abs/1710.10903
    def __init__(self, in_features, out_features, dropout, alpha, concat=True):
        super(GraphAttentionLayer, self).__init__()
        self.dropout = dropout
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha
        self.concat = concat

        self.W = nn.Parameter(torch.empty(size=(in_features, out_features)))
        # 用正态分布初始化参数
        # 其中参数值采样自均值为0,标准差为 gain * sqrt(2 / (fan_in + fan_out))
        # 也就是论文中提到的Glorot初始化
        # a和W可以用来计算论文中的attention coefficients
        nn.init.xavier_uniform_(self.W.data, gain=1.414)
        self.a = nn.Parameter(torch.empty(size=(2*out_features, 1)))    #注意力机制,因为输出为一个值,所以第二个维度为1
        nn.init.xavier_uniform_(self.a.data, gain=1.414)

        self.leakyrelu = nn.LeakyReLU(self.alpha)

    def forward(self, h, adj):
        # 共享线性变换,计算各个点与其邻居节点的attention coefficients #
        #  1. 矩阵乘法计算Wh
        Wh = torch.mm(h, self.W) # h.shape: (N, in_features), Wh.shape: (N, out_features)
        #  2. 返回类型为(N, N, 2 * out_features), 用于计算attention coefficients
        #     因为是计算N个点的coefficients,所以前面是N*N的(可能有N个邻居节点,类似加权邻接矩阵)
        a_input = self._prepare_attentional_mechanism_input(Wh)
        #  3.matmul为高维矩阵乘法,a_input为(N, N, 2 * out_features), a为(2 * out_features, 1),得到结果为(N, N, 1)
        #    squeeze(1)表示去除维度2,形状变为(N, N),表示各个节点和其他各节点之间的coefficients
        #    如论文所示使用leakyrelu
        e = self.leakyrelu(torch.matmul(a_input, self.a).squeeze(2))

        zero_vec = -9e15*torch.ones_like(e)
        # 如果为节点的一阶邻接节点(邻居),就是用计算出来的coefficients,否则使用zero_vec中的默认值
        # 所以为了可以直接使用矩阵运算,并不像文中说的只计算邻居节点,或者理解为只使用邻居节点
        attention = torch.where(adj > 0, e, zero_vec)

        # softmax按维度1归一化(每一行)
        attention = F.softmax(attention, dim=1)
        attention = F.dropout(attention, self.dropout, training=self.training)
        # 最后使用归一化的注意力系数计算节点最后的输出特征,Wh前面已经计算过了
        h_prime = torch.matmul(attention, Wh)

        # 使用是否非线性运算
        if self.concat:
            return F.elu(h_prime)
        else:
            return h_prime

    def _prepare_attentional_mechanism_input(self, Wh):
        N = Wh.size()[0] # number of nodes

        # Below, two matrices are created that contain embeddings in their rows in different orders.
        # (e stands for embedding)
        # These are the rows of the first matrix (Wh_repeated_in_chunks): 
        # e1, e1, ..., e1,            e2, e2, ..., e2,            ..., eN, eN, ..., eN
        # '-------------' -> N times  '-------------' -> N times       '-------------' -> N times
        # 
        # These are the rows of the second matrix (Wh_repeated_alternating): 
        # e1, e2, ..., eN, e1, e2, ..., eN, ..., e1, e2, ..., eN 
        # '----------------------------------------------------' -> N times
        #

        # 扩展
        # 按0维扩展,变为N*N行,原来每一行连续重复N次,形状变为(N*N, out)
        Wh_repeated_in_chunks = Wh.repeat_interleave(N, dim=0)
        # 各维度分别扩展N倍和1倍,形状变为(N*N, out),和repeat_interleave不同的是扩展时是整体扩展
        # 也就是各个矩阵连续重复N次
        Wh_repeated_alternating = Wh.repeat(N, 1)
        # Wh_repeated_in_chunks.shape == Wh_repeated_alternating.shape == (N * N, out_features)

        # The all_combination_matrix, created below, will look like this (|| denotes concatenation):
        # e1 || e1
        # e1 || e2
        # e1 || e3
        # ...
        # e1 || eN
        # e2 || e1
        # e2 || e2
        # e2 || e3
        # ...
        # e2 || eN
        # ...
        # eN || e1
        # eN || e2
        # eN || e3
        # ...
        # eN || eN

        all_combinations_matrix = torch.cat([Wh_repeated_in_chunks, Wh_repeated_alternating], dim=1)
        # all_combinations_matrix.shape == (N * N, 2 * out_features)

        return all_combinations_matrix.view(N, N, 2 * self.out_features)

    def __repr__(self):
        return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'


# 完成稀疏矩阵乘法
class SpecialSpmmFunction(torch.autograd.Function):
    # Special function for only sparse region backpropataion layer.
    @staticmethod
    def forward(ctx, indices, values, shape, b):
        assert indices.requires_grad == False
        a = torch.sparse_coo_tensor(indices, values, shape)
        ctx.save_for_backward(a, b)
        ctx.N = shape[0]
        return torch.matmul(a, b)

    @staticmethod
    def backward(ctx, grad_output):
        a, b = ctx.saved_tensors
        grad_values = grad_b = None
        if ctx.needs_input_grad[1]:
            grad_a_dense = grad_output.matmul(b.t())
            edge_idx = a._indices()[0, :] * ctx.N + a._indices()[1, :]
            grad_values = grad_a_dense.view(-1)[edge_idx]
        if ctx.needs_input_grad[3]:
            grad_b = a.t().matmul(grad_output)
        return None, grad_values, None, grad_b


class SpecialSpmm(nn.Module):
    def forward(self, indices, values, shape, b):
        return SpecialSpmmFunction.apply(indices, values, shape, b)

    
class SpGraphAttentionLayer(nn.Module):
    # Sparse version GAT layer, similar to https://arxiv.org/abs/1710.10903

    def __init__(self, in_features, out_features, dropout, alpha, concat=True):
        super(SpGraphAttentionLayer, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.alpha = alpha
        self.concat = concat

        self.W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
        nn.init.xavier_normal_(self.W.data, gain=1.414)
                
        self.a = nn.Parameter(torch.zeros(size=(1, 2*out_features)))
        nn.init.xavier_normal_(self.a.data, gain=1.414)

        self.dropout = nn.Dropout(dropout)
        self.leakyrelu = nn.LeakyReLU(self.alpha)
        self.special_spmm = SpecialSpmm()

    def forward(self, input, adj):
        dv = 'cuda' if input.is_cuda else 'cpu'

        N = input.size()[0]
        edge = adj.nonzero().t()    # 形状转换为(2,E),E为所有相连边的数量

        h = torch.mm(input, self.W)    # 共享线性变换
        # h: N x out
        assert not torch.isnan(h).any()

        # Self-attention on the nodes - Shared attention mechanism
        # 拼接所有相连边转换后的特征向量,edge_h形状为(2 x out, E)
        edge_h = torch.cat((h[edge[0, :], :], h[edge[1, :], :]), dim=1).t()
        # edge: 2*D x E

        # self.a.mm(edge_h)只计算图中存在的边,self.a形状为(1, 2 x out),与edge_h相乘得到为形状为(1,E)
        # squeeze去除其中维度值为1的维度,最终得到一个形状为(N)的一维向量
        # 但是这里只包含了相连边的节点
        edge_e = torch.exp(-self.leakyrelu(self.a.mm(edge_h).squeeze()))
        assert not torch.isnan(edge_e).any()
        # edge_e: E

        # 计算每一行的和,进行归一化时使用
        e_rowsum = self.special_spmm(edge, edge_e, torch.Size([N, N]), torch.ones(size=(N,1), device=dv))
        # e_rowsum: N x 1

        edge_e = self.dropout(edge_e)
        # edge_e: E

        h_prime = self.special_spmm(edge, edge_e, torch.Size([N, N]), h)
        assert not torch.isnan(h_prime).any()
        # h_prime: N x out

        # 在最后才进行了归一化
        h_prime = h_prime.div(e_rowsum)
        # h_prime: N x out
        assert not torch.isnan(h_prime).any()

        if self.concat:
            # if this layer is not last layer,
            return F.elu(h_prime)
        else:
            # if this layer is last layer,
            return h_prime

    def __repr__(self):
        return self.__class__.__name__ + ' (' + str(self.in_features) + ' -> ' + str(self.out_features) + ')'

    
class GAT(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout, alpha, nheads):
        # Dense version of GAT.
        super(GAT, self).__init__()
        self.dropout = dropout

        self.attentions = [GraphAttentionLayer(nfeat, nhid, dropout=dropout, alpha=alpha, concat=True) for _ in range(nheads)]
        for i, attention in enumerate(self.attentions):
            self.add_module('attention_{}'.format(i), attention)

        self.out_att = GraphAttentionLayer(nhid * nheads, nclass, dropout=dropout, alpha=alpha, concat=False)

    def forward(self, x, adj):
        x = F.dropout(x, self.dropout, training=self.training)
        x = torch.cat([att(x, adj) for att in self.attentions], dim=1)
        x = F.dropout(x, self.dropout, training=self.training)
        x = F.elu(self.out_att(x, adj))
        return F.log_softmax(x, dim=1)


class SpGAT(nn.Module):
    def __init__(self, nfeat, nhid, nclass, dropout, alpha, nheads):
        # Sparse version of GAT
        super(SpGAT, self).__init__()
        self.dropout = dropout

        self.attentions = [SpGraphAttentionLayer(nfeat, 
                                                 nhid, 
                                                 dropout=dropout, 
                                                 alpha=alpha, 
                                                 concat=True) for _ in range(nheads)]
        for i, attention in enumerate(self.attentions):
            self.add_module('attention_{}'.format(i), attention)

        self.out_att = SpGraphAttentionLayer(nhid * nheads, 
                                             nclass, 
                                             dropout=dropout, 
                                             alpha=alpha, 
                                             concat=False)

    def forward(self, x, adj):
        x = F.dropout(x, self.dropout, training=self.training)
        x = torch.cat([att(x, adj) for att in self.attentions], dim=1)
        x = F.dropout(x, self.dropout, training=self.training)
        x = F.elu(self.out_att(x, adj))
        return F.log_softmax(x, dim=1)
"""
    )


def print_plot_graph():
    print(
        """
def plot_graph():
    graph = nx.MultiGraph()
    graph.add_edges_from(edge_list)

    # 绘制图拓扑结构
    def map_node_color(node_labels, color_map):
        #生成对应label的颜色
        colors = []
        for node_label in node_labels:
            colors.append(color_map[node_label])
        
        return colors

    def map_node_alpha(node_labels, alpha_map):
        #生成对应label的颜色
        alphas = []
        for node_label in node_labels:
            alphas.append(alpha_map[node_label])
            
        return alphas

    def map_node_size(node_labels, size_map):
        #生成对应label的颜色
        sizes = []
        for node_label in node_labels:
            sizes.append(size_map[node_label])
            
        return sizes

    def plot_graph(graph, figsize=(10, 10), dpi=300, with_labels=False, node_size=1, node_color='r', alpha=0.4, save_path=None):
        display.set_matplotlib_formats('svg')
        fig = plt.figure(figsize=figsize, dpi=dpi)
        pos = nx.spring_layout(graph, iterations=200)
        nx.draw(graph, pos=pos, with_labels=with_labels, node_size=node_size, node_color=node_color, alpha=alpha, linewidths=0.5)
        # plt.show()
        if save_path is not None:
            fig.savefig(save_path, dpi=dpi)
        #   fig.savefig('scatter.eps',dpi=600,format='eps')

    
"""

    )



if __name__ == "__main__":
    pass
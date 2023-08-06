import numpy as np
import torch

class EarlyStopping:
    """This code is modified from https://zhuanlan.zhihu.com/p/350982073
    """

    def __init__(self, patience=5, delta=0, monitor='val_acc', dump_file='model.pkl', verbose=False):
        """Early stops the training if validation loss or accuracy doesn't improve after a given patience.

        Parameters
        ----------
        patience : int, optional
            How long to wait after last time val_loss/val_acc improved, by default 5
        delta : int, optional
            Minimum change in the monitored quantity to qualify as an improvement, by default 0
        monitor : str, optional
            'val_acc' or 'val_loss', by default 'val_acc'
        dump_file : str, optional
            [description], by default 'model.pkl'
        verbose : bool, optional
            If True, prints a message for each val_loss/val_acc improvement, by default False
        """
        assert monitor in ['val_acc', 'val_loss']
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.delta = delta
        self.monitor = monitor
        self.val_loss_min = np.Inf
        self.val_acc_max = 0
        self.dump_file = dump_file


    def __call__(self, model, val_loss=0, val_acc=0):

        score = -val_loss if self.monitor == 'val_loss' else val_acc

        if self.best_score is None or score >= self.best_score + self.delta:
            self.best_score = score
            self.counter = 0
            log = self.save_checkpoint(model, val_loss, val_acc)
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True
            log = (f'EarlyStopping counter: {self.counter}/{self.patience}. '
                f'Current best {self.monitor}: {self.best_score:.6f}')
        if self.verbose:
            print(log)
        return log

    def save_checkpoint(self, model, val_loss=0, val_acc=0):
        '''
        Saves model when validation loss decrease or validation accuracy increase.
        '''
        torch.save(model, self.dump_file)
        if self.monitor == 'val_loss':
            pre, post = self.val_loss_min, val_loss
        elif self.monitor == 'val_acc':
            pre, post = self.val_acc_max, val_acc
        self.val_loss_min = val_loss
        self.val_acc_max = val_acc
        return f'{self.monitor}: {pre:.6f} -> {post:.6f}, best model saved.'

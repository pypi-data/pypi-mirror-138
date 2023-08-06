import numpy as np
import math
from scipy.sparse import eye, kron, diags, vstack, spdiags, coo_matrix

def grid_graph(w, h):
    px = spdiags(np.ones(w), 1, w, w)
    py = spdiags(np.ones(h), 1, h, h)
    A = kron(py, eye(w)) + kron(eye(h), px)
    return A + A.T

def optimizing_permutation(m):
    h, w = m.shape
    A = grid_graph(w, h)
    m = A**3 @ m.flatten()
    p = np.vstack([np.argwhere(m), np.argwhere(m == 0)])
    P = coo_matrix((np.ones(h*w), (np.arange(h*w), p[:,0])), shape=(h*w, h*w))
    return P

def grid_directional_BC(w,h):
    x = spdiags(np.ones(w),1,w-1,w) - eye(w-1,w)
    Bx = kron(eye(h), x)
    Cx = abs(Bx)/2
    y = spdiags(np.ones(h),1,h-1,h) - eye(h-1,h)
    By = kron(y, eye(w))
    Cy = abs(By)/2
    return Bx, By, Cx, Cy

def incidence_and_centering_matrices(w, h):
    x = spdiags(np.ones(w),1,w-1,w) - eye(w-1,w)
    Bx = kron(eye(h), x)
    y = spdiags(np.ones(h),1,h-1,h) - eye(h-1,h)
    By = kron(y, eye(w))
    B = vstack([Bx, By])
    C = abs(B)/2
    return B, C

def incidence_matrix(w, h):
    x = spdiags(np.ones(w),1,w-1,w) - eye(w-1,w)
    Bx = kron(eye(h), x)
    y = spdiags(np.ones(h),1,h-1,h) - eye(h-1,h)
    By = kron(y, eye(w))
    B = vstack([Bx, By])
    return B

def anisotropic_incidence_matrix(w, h, a, b):
    x = spdiags(np.ones(w),1,w-1,w) - eye(w-1,w)
    Bx = a * kron(eye(h), x)
    y = spdiags(np.ones(h),1,h-1,h) - eye(h-1,h)
    By = b * kron(y, eye(w))
    B = vstack([Bx, By])
    return B

def grid_centered_gradient(w,h):
    data_x = np.vstack([-np.hstack([np.ones(w-2),0,0,0])/2,np.hstack([0,0,np.ones(w-2),0])/2])
    data_y = np.vstack([-np.hstack([np.ones(h-2),0,0,0])/2,np.hstack([0,0,np.ones(h-2),0])/2])
    diags = np.array([-1,1])
    Dx = kron(eye(h), spdiags(data_x, diags, w, w))
    Dy = kron(spdiags(data_y, diags, h, h), eye(w))
#    Dx = kron(eye(h), (eye(w,w,1) - eye(w,w,-1))/2)
#    Dx = Dx.tocsr()[np.array((np.sum(Dx,1)).T)[0] == 0,:].tocoo()
#    Dy = kron((eye(h,h,1) - eye(h,h,-1))/2, eye(w))
#    Dy = Dy.tocsr()[np.array((np.sum(Dy,1)).T)[0] == 0,:].tocoo()
    return Dx, Dy
#def grid_centered_gradient(w,h):
#    Bx, By, Cx, Cy = grid_directional_BC(w,h)
#    Dx = Cx.T @ Bx
#    Dx[np.array((np.sum(abs(-Bx.T @ Bx),1)).T)[0] == 2,:] = 0
#    Dx.eliminate_zeros()
#    Dy = Cy.T @ By
#    Dy[np.array((np.sum(abs(-By.T @ By),1)).T)[0] == 2,:] = 0
#    Dy.eliminate_zeros()
#    return Dx, Dy

def grid_second_derivative(w,h):
    Bx, By, _, _ = grid_directional_BC(w,h)
    Dxx = -Bx.T @ Bx
#    Dxx[np.array((np.sum(abs(Dxx),1)).T)[0] == 2,:] = 0
#    Dxx.eliminate_zeros()
    Dyy = -By.T @ By
#    Dyy[np.array((np.sum(abs(Dyy),1)).T)[0] == 2,:] = 0
#    Dyy.eliminate_zeros()
    Dx, Dy = grid_centered_gradient(w,h)
    Dxy = Dy @ Dx
    return Dxx, Dyy, Dxy

def local_mean(A):
    h, w = A.shape 
    _, C = incidence_and_centering_matrices(w,h)
    return (C.T @ C @ A.flatten() - A.flatten()).reshape([h,w])
    # return (4 * C.T @ C @ A + A) / 5
    #return C.T @ C @ A
    
    
def poisson(gradx_f, grady_f, g, m):
    from scikits.umfpack import spsolve
    h, w = m.shape
    #Dx, Dy = grid_centered_gradient(w,h)
    Bx, By, Cx, Cy = grid_directional_BC(w,h)
    B, _ = incidence_and_centering_matrices(w,h)
    M = diags(m.flatten())
    I = eye(w*h)
    A = I - M - M @ (B.T @ B)
    b = (I - M) @ g.flatten() + M @ (Cx.T @ Bx @ gradx_f + Cy.T @ By @ grady_f)
    u = spsolve(A,b)
    #out = g.flatten()
    #out[m.flatten() > 0] = u
    return u.reshape(h,w)




#def grid_incidence(w,h):
#    # build the incidence matrix of a grid graph
#        x = sparse(1:w-1, 2:w, 1, w-1, w) - speye(w-1,w);  # path of length W
#        y = sparse(1:h-1, 2:h, 1, h-1, h) - speye(h-1,h);  # path of length H
#        B = [ kron(speye(h),x) ; kron(y,speye(w)) ];       # kronecker union
#end

#    Dxx = -Bx.T @ Bx
#    Dxx[np.array((np.sum(abs(Dxx),1)).T)[0] == 2,:] = 0
#    Dxx.eliminate_zeros()
#
#    Dyy = -By.T @ By
#    Dyy[np.array((np.sum(abs(Dyy),1)).T)[0] == 2,:] = 0
#    Dyy.eliminate_zeros()
#
#    Dxy = Dy @ Dx

def qauto(x, p=0):
    from numpy import float, uint8
    if p > 0:
           from numpy import percentile
           m = percentile(x, p)
           M = percentile(x, 100-p)
           X = (((x.astype(float) - m)/(M-m)).clip(0,1)*255.0).astype(uint8)
    else:
          m = x.min()
          M = x.max()
          X  = (255 * (x.astype(float) - m) / (M - m) ).astype(uint8)
    return X


def simplest_color_balance(im):
    min_im = np.percentile(im,2)
    max_im = np.percentile(im,98)

    return

# Horn's more complicated gradient 
def gradient_stencil_shift(w, h):
    # gradient with staggered grids (Horn & Schunck, 1981)
    diag = np.array([0, 1])
    
    submat_x = spdiags(np.vstack([ - np.ones(w), np.ones(w)]) / 2, 
                       diag, w - 1, w)
    mat_x = spdiags(np.vstack([ np.ones(h), np.ones(h)]), diag, h - 1, h)
    
    submat_y = spdiags(np.vstack([np.ones(w), np.ones(w)]) / 2, 
                       diag, w - 1, w)
    mat_y = spdiags(np.vstack([ - np.ones(h), np.ones(h)]), diag, h - 1, h)
   
    return kron(mat_x, submat_x), kron(mat_y, submat_y)

def laplacian_diagonal(w, h):
    # associated laplacia
    Bx, By = gradient_stencil_shift(w, h)
    return - (Bx.T @ Bx + By.T @ By)

def local_mean_diagonal(A):
    h, w = A.shape 
    L = laplacian_diagonal(w, h) 
    return (L @ A.flatten() / 2 + A.flatten()).reshape([h,w])
 
def flat_local_mean_diagonal(A, w, h):
    L = laplacian_diagonal(w, h)
    return (L @ A / 2 + A)


def flat_local_mean_diagonal_inside(A, Bx, By):
    L = - (Bx.T @ Bx + By.T @ By)
    return (L @ A / 2 + A)

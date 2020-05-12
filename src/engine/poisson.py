from nptyping import Array


class Poisson(object):
    """
    This class describes the abstracts part of the Poisson equation
    """

    def __init__(self):  # , mode_boundary=1, mode_poisson=0):
        self.EXPLICIT = 0
        self.IMPLICIT = 1

        self.NEUMANN = 0
        self.DIRICHLET = 1

        self._mode_poisson = self.EXPLICIT
        self._mode_boundary = self.DIRICHLET
        self.alpha = 0.25

    @property
    def boundary(self):
        """
        Returns the boundary mode (Neumann or Dirichlet)

        Returns
        -------
        int
            the boundary mode
        """
        return self._mode_boundary

    @property
    def mode_boundary(self):
        """
        Returns the boundary mode (Neumann or Dirichlet)

        Returns
        -------
        int
            the boundary mode
        """
        return self._mode_boundary

    @mode_boundary.setter
    def mode_boundary(self, mode):
        """
        Sets the boundary mode (Neumann or Dirichlet)

        Parameters
        -------
        mode
            the boundary mode
        """
        self.set_boundary(mode)

    @property
    def mode_poisson(self):
        """
        Gets the Poisson mode (explicit or implicit)
        """
        return self._mode_poisson

    @mode_poisson.setter
    def mode_poisson(self, mode):
        """
        Sets the Poisson mode (explicit or implicit)

        Parameters
        -------
        mode
            the Poisson mode

        """
        if mode == "Explicit" or mode == self.EXPLICIT:
            self._mode_poisson = self.EXPLICIT
        elif mode == "Implicit" or mode == self.IMPLICIT:
            self._mode_poisson = self.IMPLICIT
        else:
            raise Exception("Illegal mode ({})".format(mode))

    def set_boundary(self, mode):
        """
        Sets the boundary mode

        Parameters
        -------
        mode
            the boundary mode
        """
        if (type(mode) == str and mode.lower() == "Dirichlet".lower()) or mode == self.DIRICHLET:
            self._mode_boundary = self.DIRICHLET
        elif (type(mode) == str and mode.lower() == "Neumann".lower()) or mode == self.NEUMANN:
            self._mode_boundary = self.NEUMANN
        else:
            raise Exception("Illegal boundary ({})".format(mode))

    def set_mode(self, mode):
        """
        Sets the Poisson mode

        Parameters
        -------
        mode
            the Poisson mode
        """
        if mode == "Explicit" or mode == self.EXPLICIT:
            self._mode_poisson = self.EXPLICIT
        elif mode == "Implicit" or mode == self.IMPLICIT:
            self._mode_poisson = self.IMPLICIT
        else:
            raise Exception("Illegal mode ({})".format(mode))

    def __str__(self):
        """
        Returns a string representation of the object.

        Returns
        -------
        str
            the string representation
        """
        return ("Neumann" if self.mode_boundary == self.NEUMANN else "Diriclet") + \
               " with " + \
               ("Explicit" if self.mode_poisson == self.EXPLICIT else "Implicit") + \
               " and " + \
               "alpha = " + str(self.alpha)

    def __repr__(self):
        """
        Returns a unambiguous string representation of the object (for debug...).

        Returns
        -------
        str
            the string representation
        """
        return self.__str__()

    def set_alpha(self, value: float):
        """
        Set the alpha value

        Parameters
        ----------
        value : float
            The alpha value
        """
        self.alpha = value

    def get_laplace_explicit(self, data: Array[float, float] = None, alpha: bool = True) -> Array:
        """
        Gets the Laplace

        Parameters
        ----------
        data : ndarray
            The data to get the Laplace from
        alpha : bool
            If you want to apply the alpha directly

        Returns
        -------
        ndarray
            the Laplace array
        """
        if data is None:
            data = self.data
        laplace = data[0:-2, 1:-1] \
                  + data[2:, 1:-1] \
                  + data[1:-1, 0:-2] \
                  + data[1:-1, 2:] \
                  - 4 * data[1:-1, 1:-1]
        if not alpha:
            return laplace
        return laplace * self.alpha

    def get_laplace_implicit(self, data):
        """
        Gets the Laplace

        Parameters
        ----------
        data : ndarray
            The data to get the Laplace from
        """
        raise NotImplementedError("Had no time left")

    def common_shape(self, data):
        """
        Make sure the method gets the correct shape

        Parameters
        ----------
        data : ndarray
            The data to get a common shape for
        """
        if self.mode_poisson == self.EXPLICIT:
            return data[1:-1, 1:-1]
        else:
            raise NotImplementedError("Not supported")

    def get_laplace(self, data, alpha=True):
        """
        Gets the correct Laplace based on mode

        Parameters
        ----------
        data : ndarray
            The data to get the Laplace from

        Returns
        -------
        ndarray
            the Laplace array
        """
        if self.mode_poisson == self.EXPLICIT:
            return self.get_laplace_explicit(data, alpha)
        else:
            raise NotImplementedError("Not supported")

    def apply_boundary(self, data) -> Array:
        """
        Apply the boundary

        Parameters
        ----------
        data : ndarray
            The data

        Returns
        -------
        ndarray
            the new array with boundary applied
        """
        if self.mode_boundary == self.NEUMANN:
            return self.neumann(data)
        elif self.mode_boundary == self.DIRICHLET:
            return self.diriclet(data)
        else:
            raise Exception("not supported")

    def solve(self, data: Array, operator: callable, h: callable = lambda i=None: 0,
              apply_boundary: bool = True) -> Array:
        """
        Solve the Poisson equation

        Parameters
        ----------
        data : ndarray
            The data to work with
        operator : callable
            The function applied
        h : callable
            The h function
        apply_boundary: bool
            if you want to apply the set boundary

        Returns
        -------
        ndarray
            the iterated array
        """
        if self.mode_poisson == self.EXPLICIT:
            resultat = data.copy()
            if (len(data.shape) == 3):
                for i in range(3):
                    resultat[1:-1, 1:-1, i] += self.alpha * (operator(i) - h(i=i))
            else:
                resultat[1:-1, 1:-1] += self.alpha * (operator() - h(None))
        else:
            raise NotImplementedError("Not supported")

        if apply_boundary:
            return self.apply_boundary(resultat).clip(0, 1)
        else:
            return resultat.clip(0, 1)

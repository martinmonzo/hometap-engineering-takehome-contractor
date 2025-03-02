# Hometap Property Detail Search

## Implementation of an endpoint that retrieves information about a property, given its address.

This is an excercise that consists of a **backend** and a **frontend** to retrieve information about a property.

### Architecture
1. Backend
    - The backend consists of a **Layer architecture** - View, Service and Provider. Each layer is descripted below:
        - View: Is the controller that manages the input from the Frontend and maps the request to an endpoint. It
        communicates to the service and should only have dependency with this layer.
        - Service: This is the layer that has the business logic. It's called by the controller and it calls to the providers
        to communicate with third party APIs.
            - It is able to use one provider if another fails.
            - It handles the providers responses, and returns the errors if all of them failed.
        - Provider: It's responsible of isolate the logic to communicate with third parties and retrieve information to the service.
            - Both providers inherit from a base provider in order to provide flexibility to add new providers in the future.

    This architecture reduces the dependencies among the components and limits the responsibilities of each class, alowing flexibility and
    mantainability of the system if there are changes in the future.

2. Frontend
    - A React app that calls the Backend endpoint and shows the response in a friendly way to the user.
    - There are some improvements like:
        - Styling
        - Efficiency: Avoid calling the endpoint if the address is empty or if a call is in progress.

### Ideas for extending the solution
1. Cache the addresses for a reasonable period (e.g. 1 day, or at least a few minutes, depending on how often the information may change)
2. Add models to save the data
3. Add Repository layer (similar to provider, but it's responsible to communicate with Models instead of third party APIs)
4. Have more endpoints, services, etc. by adding new functionalities to the whole system, for example:
    - Manage my properties
    - See available properties in a map
    - Compare properties
    - User authentication

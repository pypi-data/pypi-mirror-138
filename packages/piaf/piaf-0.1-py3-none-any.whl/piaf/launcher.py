# coding: utf-8
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Collection, List, Mapping, Type
from piaf.comm.mts import MessageTransportProtocol
from piaf.exceptions import InvalidStateException

from piaf.platform import AgentPlatform, PlatformState


@dataclass(eq=True, frozen=True)
class ServiceDescription:
    """Description of a service to be launched by a :class:`PlatformLauncher` instance."""

    #: The :class:`AID` short name
    name: str

    #: The class
    clazz: Type

    #: A collection of arguments to be passed to the constructors
    args: Collection[Any] = field(default_factory=list)

    #: Same as  `args` but for keyword arguments
    kwargs: Mapping[str, Any] = field(default_factory=dict)


AgentDescription = ServiceDescription
AgentDescription.__doc__ = """Description of an agent to be launched by a :class:`PlatformLauncher` instance."""


class PlatformLauncher:
    """
    A simpler API to create, set up, launch and teardown a platform.

    Once the :class:`PlatformLauncher` instance is created, you can add agents, services and MTPs. Once ready, just
    call the :meth:`run` method. It will launch the platform and wait for you to hit Ctrl + C.
    """

    def __init__(self, ptf_name: str) -> None:
        """
        Create a new :class:`PlatformLauncher` instance.

        Initially, there is no agents, services or MTPs registered and the platform is created but not launched.

        :param ptf_name: name of the platform
        """
        self.ptf = AgentPlatform(ptf_name)
        self._agents: List[AgentDescription] = []
        self._services: List[ServiceDescription] = []
        self._mtps: List[MessageTransportProtocol] = []

    def add_agent(self, agent_description: AgentDescription) -> None:
        """
        Add the given agent to the platform.

        :param agent_description: description of the agent to add
        :raise InvalidStateException: the platform is already launched
        """
        if self.ptf.state != PlatformState.INITIALIZED:
            raise InvalidStateException(self.ptf.state, "add_agent")
        self._agents.append(agent_description)

    def add_service(self, service_description: ServiceDescription) -> None:
        """
        Add the given service to the platform.

        :param service_description: description of the service to add
        :raise InvalidStateException: the platform is already launched
        """
        if self.ptf.state != PlatformState.INITIALIZED:
            raise InvalidStateException(self.ptf.state, "add_service")
        self._services.append(service_description)

    def add_mtp(self, mtp: MessageTransportProtocol) -> None:
        """
        Add the given MTP to the platform.

        :param mtp: the instantiated MTP
        :raise InvalidStateException: the platform is already launched
        """
        if self.ptf.state != PlatformState.INITIALIZED:
            raise InvalidStateException(self.ptf.state, "add_mtp")
        self._mtps.append(mtp)

    def run(self) -> None:
        """
        Configure and run the wrapped :class:`AgentPlatform`.

        This method takes care of getting the event loop and tearing down things. Control is given back en CTRL+C.
        """
        loop = asyncio.get_event_loop()
        try:
            loop.create_task(self._main())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(self.ptf.stop())
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    async def _main(self) -> None:
        """Coroutine that starts the platform and setup mtps, services and agents."""
        # Before adding anything, we need to start the platform. This ensure that the
        # AMS agent is created
        await self.ptf.start()

        # Then register all provided MTP instances
        for mtp in self._mtps:
            await self.ptf.acc.register_mtp(mtp)

        # Then services
        for service in self._services:
            aid = await self.ptf.agent_manager.create(
                service.clazz, service.name, True, *service.args, **service.kwargs
            )
            await self.ptf.agent_manager.invoke(aid)

        # Then agents
        for agent in self._agents:
            aid = await self.ptf.agent_manager.create(
                agent.clazz, agent.name, True, *agent.args, **agent.kwargs
            )
            await self.ptf.agent_manager.invoke(aid)

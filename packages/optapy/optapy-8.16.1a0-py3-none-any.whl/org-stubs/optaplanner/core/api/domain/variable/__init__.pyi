import java.io
import java.lang
import java.lang.annotation
import java.util
import org.optaplanner.core.api.score.director
import org.optaplanner.core.impl.heuristic.selector.common.decorator
import typing



class AnchorShadowVariable(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface AnchorShadowVariable
    
        Specifies that a bean property (or a field) is the anchor of a chained
        :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`, which implies it's a shadow variable.
    
        It is specified on a getter of a java bean property (or a field) of a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def sourceVariableName(self) -> str: ...
    def toString(self) -> str: ...

class InverseRelationShadowVariable(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface InverseRelationShadowVariable
    
        Specifies that a bean property (or a field) is the inverse of a
        :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`, which implies it's a shadow variable.
    
        It is specified on a getter of a java bean property (or a field) of a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def sourceVariableName(self) -> str: ...
    def toString(self) -> str: ...

class PlanningVariable(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface PlanningVariable
    
        Specifies that a bean property (or a field) can be changed and should be optimized by the optimization algorithms.
    
        It is specified on a getter of a java bean property (or directly on a field) of a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def graphType(self) -> 'PlanningVariableGraphType': ...
    def hashCode(self) -> int: ...
    def nullable(self) -> bool: ...
    def strengthComparatorClass(self) -> typing.Type[java.util.Comparator]: ...
    def strengthWeightFactoryClass(self) -> typing.Type[org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory]: ...
    def toString(self) -> str: ...
    def valueRangeProviderRefs(self) -> typing.List[str]: ...
    class NullStrengthComparator(java.util.Comparator):
        def equals(self, object: typing.Any) -> bool: ...
    class NullStrengthWeightFactory(org.optaplanner.core.impl.heuristic.selector.common.decorator.SelectionSorterWeightFactory): ...

class PlanningVariableGraphType(java.lang.Enum['PlanningVariableGraphType']):
    """
    public enum PlanningVariableGraphType extends :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.Enum?is`<:class:`~org.optaplanner.core.api.domain.variable.PlanningVariableGraphType`>
    """
    NONE: typing.ClassVar['PlanningVariableGraphType'] = ...
    CHAINED: typing.ClassVar['PlanningVariableGraphType'] = ...
    _valueOf_0__T = typing.TypeVar('_valueOf_0__T', bound=java.lang.Enum)  # <T>
    @typing.overload
    @staticmethod
    def valueOf(class_: typing.Type[_valueOf_0__T], string: str) -> _valueOf_0__T: ...
    @typing.overload
    @staticmethod
    def valueOf(string: str) -> 'PlanningVariableGraphType':
        """
            Returns the enum constant of this type with the specified name. The string must match *exactly* an identifier used to
            declare an enum constant in this type. (Extraneous whitespace characters are not permitted.)
        
            Parameters:
                name (:class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.String?is`): the name of the enum constant to be returned.
        
            Returns:
                the enum constant with the specified name
        
            Raises:
                :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.IllegalArgumentException?is`: if this enum type has no constant with the specified name
                :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.NullPointerException?is`: if the argument is null
        
        
        """
        ...
    @staticmethod
    def values() -> typing.List['PlanningVariableGraphType']:
        """
            Returns an array containing the constants of this enum type, in the order they are declared. This method may be used to
            iterate over the constants as follows:
        
            .. code-block: java
            
            for (PlanningVariableGraphType c : PlanningVariableGraphType.values())
                System.out.println(c);
            
        
            Returns:
                an array containing the constants of this enum type, in the order they are declared
        
        
        """
        ...

class PlanningVariableReference(java.lang.annotation.Annotation):
    """
    public @interface PlanningVariableReference
    
        A reference to a genuine :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable` or a shadow variable.
    """
    def entityClass(self) -> typing.Type[typing.Any]: ...
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def toString(self) -> str: ...
    def variableName(self) -> str: ...
    class NullEntityClass: ...

_VariableListener__Solution_ = typing.TypeVar('_VariableListener__Solution_')  # <Solution_>
_VariableListener__Entity_ = typing.TypeVar('_VariableListener__Entity_')  # <Entity_>
class VariableListener(java.io.Closeable, typing.Generic[_VariableListener__Solution_, _VariableListener__Entity_]):
    """
    public interface VariableListener<Solution_, Entity_> extends :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.io.Closeable?is`
    
        Changes shadow variables when a genuine planning variable changes.
    
        Important: it must only change the shadow variable(s) for which it's configured! It should never change a genuine
        variable or a problem fact. It can change its shadow variable(s) on multiple entity instances (for example: an
        arrivalTime change affects all trailing entities too).
    
        It is recommended that implementations be kept stateless. If state must be implemented, implementations may need to
        override the default methods (:meth:`~org.optaplanner.core.api.domain.variable.VariableListener.resetWorkingSolution`,
        :meth:`~org.optaplanner.core.api.domain.variable.VariableListener.close`).
    """
    def afterEntityAdded(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def afterEntityRemoved(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def afterVariableChanged(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def beforeEntityAdded(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def beforeEntityRemoved(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def beforeVariableChanged(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_], entity_: _VariableListener__Entity_) -> None: ...
    def close(self) -> None:
        """
            Called before this :class:`~org.optaplanner.core.api.domain.variable.VariableListener` is thrown away and not used
            anymore.
        
            Specified by:
                
                meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.AutoCloseable.html?is` in
                interface :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.AutoCloseable?is`
        
            Specified by:
                :meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.io.Closeable.html?is` in
                interface :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.io.Closeable?is`
        
        
        """
        ...
    def requiresUniqueEntityEvents(self) -> bool:
        """
            When set to :code:`true`, this has a slight performance loss in Planner. When set to :code:`false`, it's often easier to
            make the listener implementation correct and fast.
        
            Returns:
                true to guarantee that each of the before/after methods will only be called once per entity instance per operation type
                (add, change or remove).
        
        
        """
        ...
    def resetWorkingSolution(self, scoreDirector: org.optaplanner.core.api.score.director.ScoreDirector[_VariableListener__Solution_]) -> None: ...

class CustomShadowVariable(java.lang.annotation.Annotation):
    """
    :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Target?is`({:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`,:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.ElementType.html?is`}) :class:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.Retention?is`(:meth:`~org.optaplanner.core.api.domain.variable.https:.docs.oracle.com.javase.8.docs.api.java.lang.annotation.RetentionPolicy.html?is`) public @interface CustomShadowVariable
    
        Specifies that a bean property (or a field) is a custom shadow of 1 or more
        :class:`~org.optaplanner.core.api.domain.variable.PlanningVariable`'s.
    
        It is specified on a getter of a java bean property (or a field) of a
        :class:`~org.optaplanner.core.api.domain.entity.PlanningEntity` class.
    """
    def equals(self, object: typing.Any) -> bool: ...
    def hashCode(self) -> int: ...
    def sources(self) -> typing.List[PlanningVariableReference]: ...
    def toString(self) -> str: ...
    def variableListenerClass(self) -> typing.Type[VariableListener]: ...
    def variableListenerRef(self) -> PlanningVariableReference: ...
    class NullVariableListener(VariableListener): ...


class __module_protocol__(typing.Protocol):
    # A module protocol which reflects the result of ``jp.JPackage("org.optaplanner.core.api.domain.variable")``.

    AnchorShadowVariable: typing.Type[AnchorShadowVariable]
    CustomShadowVariable: typing.Type[CustomShadowVariable]
    InverseRelationShadowVariable: typing.Type[InverseRelationShadowVariable]
    PlanningVariable: typing.Type[PlanningVariable]
    PlanningVariableGraphType: typing.Type[PlanningVariableGraphType]
    PlanningVariableReference: typing.Type[PlanningVariableReference]
    VariableListener: typing.Type[VariableListener]

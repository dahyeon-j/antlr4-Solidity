# Generated from C:/Users/PLAS/PycharmProjects/antlr4_Solidity\Solidity.g4 by ANTLR 4.9.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SolidityParser import SolidityParser
else:
    from SolidityParser import SolidityParser

# This class defines a complete generic visitor for a parse tree produced by SolidityParser.

class SolidityVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SolidityParser#sourceUnit.
    """
    <class 'SolidityParser.SolidityParser.PragmaDirectiveContext'>    pragmasolidity>=0.4.0<0.6.0;
    <class 'SolidityParser.SolidityParser.ContractDefinitionContext'>    contractSimpleStorage{uintstoredData;functionset(uintx)public{storedData=x;}functionget()publicviewreturns(uint){returnstoredData;}}
    <class 'antlr4.tree.Tree.TerminalNodeImpl'>    <EOF>
    """
    def visitSourceUnit(self, ctx:SolidityParser.SourceUnitContext):
        text = ''

        text += self.visitPragmaDirective(ctx.getChild(0)) # pragma directive

        # contracts
        for i in range(1, ctx.getChildCount() - 1):
            text += self.visitContractDefinition(ctx.getChild(i))
        print(text)
        return text
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#pragmaDirective.
    def visitPragmaDirective(self, ctx:SolidityParser.PragmaDirectiveContext):

        return 'pragma ' + self.visitVersionPragma(ctx.getChild(1)) + ';\n\n'


    # Visit a parse tree produced by SolidityParser#VersionPragma.
    def visitVersionPragma(self, ctx:SolidityParser.VersionPragmaContext):
        return ctx.getChild(0).getText() + ' ' + self.visitVersion(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#version.
    def visitVersion(self, ctx:SolidityParser.VersionContext):
        if ctx.getChildCount() == 1:
            return self.visitVersionConstraint(ctx.getChild(0))
        else:
            return self.visitVersionConstraint(ctx.getChild(0)) + ' ' + self.visitVersionConstraint(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#versionOperator.
    def visitVersionOperator(self, ctx:SolidityParser.VersionOperatorContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#versionConstraint.
    def visitVersionConstraint(self, ctx:SolidityParser.VersionConstraintContext):
        if ctx.getChildCount() == 1:
            return ctx.getText()
        else:
            return self.visitVersionOperator(ctx.getChild(0)) + ctx.getChild(1).getText()
        # for child in ctx.getChildren():
        #     print(str(child.__class__) + "    " + child.getText())
        # return ''
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#contractDefinition.
    def visitContractDefinition(self, ctx:SolidityParser.ContractDefinitionContext):
        text = 'contract ' + self.visitIdentifier(ctx.getChild(1)) + ' {\n'
        for i in range(3, ctx.getChildCount() - 1):
            text += self.visitContractPart(ctx.getChild(i))
        text += '\n}'
        return text


    # Visit a parse tree produced by SolidityParser#contractPart.
    def visitContractPart(self, ctx:SolidityParser.ContractPartContext):
        return self.visit(ctx.getChild(0))
        # for child in ctx.getChildren():
        #     print(str(child.__class__) + "    " + child.getText())
        # if 'StateVariableDeclaration' in str(ctx.getChild(0).__class__):
        #     return self.visitStateVariableDeclaration(ctx.getChild(0))
        # elif 'ConstructorDefinition' in str(ctx.getChild(0).__class__):
        #     return self.visitConstructorDefinition(ctx.getChild(0))
        # elif 'FunctionDefinition' in str(ctx.getChild(0).__class__):
        #     print('?' + self.visit(ctx.getChild(0)))
        #
        #     print('!')
        #     return self.visitFunctionDefinition(ctx.getChild(0))
        # elif 'EnumDefinition' in str(ctx.getChild(0).__class__):
        #     return self.visitEnumDefinition(ctx.getChild(0))
        #
        # return ''
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by SolidityParser#stateVariableDeclaration.
    """
    <class 'antlr4.tree.Tree.TerminalNodeImpl'>    final
    <class 'SolidityParser.SolidityParser.AnnotatedTypeNameContext'>    uint
    <class 'SolidityParser.SolidityParser.IdentifierContext'>    storedData
    <class 'antlr4.tree.Tree.TerminalNodeImpl'>    ;
    <class 'antlr4.tree.Tree.TerminalNodeImpl'>    final
    <class 'SolidityParser.SolidityParser.AnnotatedTypeNameContext'>    uint
    <class 'SolidityParser.SolidityParser.IdentifierContext'>    storedData
    <class 'antlr4.tree.Tree.TerminalNodeImpl'>    ;
    """
    # Solidity.g4 72 line
    def visitStateVariableDeclaration(self, ctx:SolidityParser.StateVariableDeclarationContext):
        text = ''
        for child in ctx.getChildren():
            if child.getText() == ';':
                text += ';\n'
            elif 'TerminalNode' in str(child.__class__):
                if child.getText() == '=':
                    text += ' = '
                else:
                    text += (child.getText() + ' ')
            elif 'AnnotatedTypeName' in str(child.__class__):
                text += (self.visitAnnotatedTypeName(child) + ' ')
            elif 'Identifier' in str(child.__class__):
                text += self.visitIdentifier(child)
            else:
                text += self.visit(child)

        return text

    # Visit a parse tree produced by SolidityParser#constructorDefinition.
    def visitConstructorDefinition(self, ctx:SolidityParser.ConstructorDefinitionContext):
        return 'constructor' + self.visitParameterList(ctx.getChild(1)) + self.visitModifierList(ctx.getChild(2)) + self.visitBlock(ctx.getChild(3))


    # Visit a parse tree produced by SolidityParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SolidityParser.FunctionDefinitionContext):
        if ctx.getChildCount() == 5:
            return 'function ' + self.visitIdentifier(ctx.getChild(1)) + self.visitParameterList(ctx.getChild(2)) + ' ' + self.visitModifierList(ctx.getChild(3)) + ' ' + self.visitBlock(ctx.getChild(4))
        else:
            return 'function ' + self.visitIdentifier(ctx.getChild(1)) + self.visitParameterList(ctx.getChild(2))  + ' ' + self.visitModifierList(ctx.getChild(3)) + ' ' + self.visitReturnParameters(ctx.getChild(4)) + ' ' + self.visitBlock(ctx.getChild(5))


    # Visit a parse tree produced by SolidityParser#returnParameters.
    def visitReturnParameters(self, ctx:SolidityParser.ReturnParametersContext):
        return 'return ' + self.visitParameterList(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#modifierList.
    def visitModifierList(self, ctx:SolidityParser.ModifierListContext):
        if hasattr(ctx.getChild(0), 'visitStateMutability'):
            return self.visitStateMutability(ctx.getChild(0))
        else:
            return ctx.getChild(0).getText()


    # Visit a parse tree produced by SolidityParser#modifier.
    def visitModifier(self, ctx:SolidityParser.ModifierContext):
        if 'StateMutability' in str(ctx.getChild(0).__class__):
            return self.visitStateMutability(ctx.getChild(0))
        else:
            return ctx.getChild(0).getText()


    # Visit a parse tree produced by SolidityParser#parameterList.
    def visitParameterList(self, ctx:SolidityParser.ParameterListContext):
        text = '('
        for i in range(1, ctx.getChildCount() - 1):
            if 'ParameterContext' in str(ctx.getChild(i).__class__):
                text += self.visitParameter(ctx.getChild(i))
            else:
                text += ', '
        text += ')'
        return text


    # Visit a parse tree produced by SolidityParser#parameter.
    def visitParameter(self, ctx:SolidityParser.ParameterContext):
        text = ''
        for child in ctx.getChildren():
            if 'Identifier' in str(child.__class__):
                text += (' ' + self.visitIdentifier(child))
            elif 'AnnotatedTypeNameContext' in str(child.__class__):
                text += self.visitAnnotatedTypeName(child)
            else:
                text += (child.getText + ' ')

        return text


    # Visit a parse tree produced by SolidityParser#enumValue.
    def visitEnumValue(self, ctx:SolidityParser.EnumValueContext):
        return self.visitIdentifier(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#enumDefinition.
    def visitEnumDefinition(self, ctx:SolidityParser.EnumDefinitionContext):

        return ''


    # Visit a parse tree produced by SolidityParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:SolidityParser.VariableDeclarationContext):
        return ''



    # Visit a parse tree produced by SolidityParser#typeName.
    def visitTypeName(self, ctx:SolidityParser.TypeNameContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#userDefinedTypeName.
    def visitUserDefinedTypeName(self, ctx:SolidityParser.UserDefinedTypeNameContext):
        return ''



    # Visit a parse tree produced by SolidityParser#mapping.
    def visitMapping(self, ctx:SolidityParser.MappingContext):
        return ''



    # Visit a parse tree produced by SolidityParser#stateMutability.
    def visitStateMutability(self, ctx:SolidityParser.StateMutabilityContext):
        return ctx.getChild(0).getText()


    # Visit a parse tree produced by SolidityParser#block.
    def visitBlock(self, ctx:SolidityParser.BlockContext):
        text = '{\n'
        for i in range(1, ctx.getChildCount() - 1):
            text += self.visitStatement(ctx.getChild(i))
        text += '}\n'
        return text


    # Visit a parse tree produced by SolidityParser#statement.
    def visitStatement(self, ctx:SolidityParser.StatementContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SolidityParser.ExpressionStatementContext):
        return self.visit(ctx.getChild(0)) + ';'


    # Visit a parse tree produced by SolidityParser#ifStatement.
    def visitIfStatement(self, ctx:SolidityParser.IfStatementContext):
        if ctx.getChildCount() == 5:
            return 'if (' + self.visit(ctx.getChild(2)) + ')' + self.visitStatement(ctx.getChild(4))
        else:
            return 'if (' + self.visit(ctx.getChild(2)) + ')' + self.visitStatement(ctx.getChild(4)) + 'else' + self.visitStatement(ctx.getChild(6))

    # Visit a parse tree produced by SolidityParser#whileStatement.
    def visitWhileStatement(self, ctx:SolidityParser.WhileStatementContext):
        return 'while (' + self.visitStatement(ctx.getChild(2)) + ')' + self.visitStatement(ctx.getChild(4))


    # Visit a parse tree produced by SolidityParser#simpleStatement.
    def visitSimpleStatement(self, ctx:SolidityParser.SimpleStatementContext):
        if 'VariableDeclarationStatement' in str(ctx.getChild(0).__class__):
            self.visitVariableDeclarationStatement(ctx.getChild(0))
        else:
            self.visitExpressionStatement(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#forStatement.
    # ToDo
    def visitForStatement(self, ctx:SolidityParser.ForStatementContext):
        return 'for'


    # Visit a parse tree produced by SolidityParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:SolidityParser.DoWhileStatementContext):
        return 'do \n' + self.visitStatement(ctx.getChild(1)) + 'while (' + self.visitExpression(ctx.getChild(4)) + ');'


    # Visit a parse tree produced by SolidityParser#continueStatement.
    def visitContinueStatement(self, ctx:SolidityParser.ContinueStatementContext):
        return 'continue;'


    # Visit a parse tree produced by SolidityParser#breakStatement.
    def visitBreakStatement(self, ctx:SolidityParser.BreakStatementContext):
        return 'break;'


    # Visit a parse tree produced by SolidityParser#returnStatement.
    def visitReturnStatement(self, ctx:SolidityParser.ReturnStatementContext):
        if ctx.getChildCount() == 3:
            return 'return' + self.visit(ctx.getChild(1)) + ';'
        else:
            return 'return;'


    # Visit a parse tree produced by SolidityParser#variableDeclarationStatement.
    def visitVariableDeclarationStatement(self, ctx:SolidityParser.VariableDeclarationStatementContext):
        if ctx.getChildCount() == 2:
            return self.visitVariableDeclaration(ctx.getChild(0)) + ';'
        else:
            return self.visitVariableDeclaration(ctx.getChild(0)) + ' = ' + self.visit(ctx.getChild(2)) + ';'


    # Visit a parse tree produced by SolidityParser#elementaryTypeName.
    def visitElementaryTypeName(self, ctx:SolidityParser.ElementaryTypeNameContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#AndExpr.
    def visitAndExpr(self, ctx:SolidityParser.AndExprContext):
        return self.visit(ctx.getChild(0)) + ' && ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#ParenthesisExpr.
    def visitParenthesisExpr(self, ctx:SolidityParser.ParenthesisExprContext):
        return '(' + self.visit(ctx.getChild(1)) + ')'


    # Visit a parse tree produced by SolidityParser#BitwiseOrExpr.
    def visitBitwiseOrExpr(self, ctx:SolidityParser.BitwiseOrExprContext):
        return self.visit(ctx.getChild(0)) + ' | ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#AllExpr.
    def visitAllExpr(self, ctx:SolidityParser.AllExprContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#IteExpr.
    # 3항 연산자
    def visitIteExpr(self, ctx:SolidityParser.IteExprContext):
        return self.visit(ctx.getChild(0)) + '? ' + self.visit(ctx.getChild(2)) + ' : ' + self.visit(ctx.getChild(4))


    # Visit a parse tree produced by SolidityParser#PowExpr.
    def visitPowExpr(self, ctx:SolidityParser.PowExprContext):
        return self.visit(ctx.getChild(0)) + ' ** ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#StringLiteralExpr.
    def visitStringLiteralExpr(self, ctx:SolidityParser.StringLiteralExprContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#PlusMinusExpr.
    def visitPlusMinusExpr(self, ctx:SolidityParser.PlusMinusExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#CompExpr.
    def visitCompExpr(self, ctx:SolidityParser.CompExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#IndexExpr.
    def visitIndexExpr(self, ctx:SolidityParser.IndexExprContext):
        return self.visit(ctx.getChild(0)) + '[' + self.visit(ctx.getChild(2)) + ']'


    # Visit a parse tree produced by SolidityParser#SignExpr.
    def visitSignExpr(self, ctx:SolidityParser.SignExprContext):
        return ctx.getChild(0).getText() + self.visit(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#NumberLiteralExpr.
    def visitNumberLiteralExpr(self, ctx:SolidityParser.NumberLiteralExprContext):
        return self.visitNumberLiteral(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#BitwiseNotExpr.
    def visitBitwiseNotExpr(self, ctx:SolidityParser.BitwiseNotExprContext):
        return '~' + self.visit(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:SolidityParser.IdentifierExprContext):
        return self.visitIdentifier(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#BooleanLiteralExpr.
    def visitBooleanLiteralExpr(self, ctx:SolidityParser.BooleanLiteralExprContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#MeExpr.
    def visitMeExpr(self, ctx:SolidityParser.MeExprContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#NotExpr.
    def visitNotExpr(self, ctx:SolidityParser.NotExprContext):
        return '!' + self.visit(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#BitShiftExpr.
    def visitBitShiftExpr(self, ctx:SolidityParser.BitShiftExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#BitwiseAndExpr.
    def visitBitwiseAndExpr(self, ctx:SolidityParser.BitwiseAndExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#MultDivModExpr.
    def visitMultDivModExpr(self, ctx:SolidityParser.MultDivModExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#AssignmentExpr.
    def visitAssignmentExpr(self, ctx:SolidityParser.AssignmentExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#TupleExpr.
    def visitTupleExpr(self, ctx:SolidityParser.TupleExprContext):
        return self.visitTupleExpression(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#OrExpr.
    def visitOrExpr(self, ctx:SolidityParser.OrExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx:SolidityParser.FunctionCallExprContext):
        return self.visit(ctx.getChild(0)) + '(' + self.visitFunctionCallArguments(ctx.getChild(2)) + ')'


    # Visit a parse tree produced by SolidityParser#EqExpr.
    def visitEqExpr(self, ctx:SolidityParser.EqExprContext):
        return self.visit(ctx.getChild(0)) + '(' + self.visitFunctionCallArguments(ctx.getChild(2)) + ')'



    # Visit a parse tree produced by SolidityParser#PostCrementExpr.
    def visitPostCrementExpr(self, ctx:SolidityParser.PostCrementExprContext):
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText()



    # Visit a parse tree produced by SolidityParser#PrimitiveCastExpr.
    def visitPrimitiveCastExpr(self, ctx:SolidityParser.PrimitiveCastExprContext):
        return self.visitElementaryTypeName(ctx.getChild(0)) + '(' + self.visit(ctx.getChild(2)) + ')'


    # Visit a parse tree produced by SolidityParser#BitwiseXorExpr.
    def visitBitwiseXorExpr(self, ctx:SolidityParser.BitwiseXorExprContext):
        return self.visit(ctx.getChild(0)) + ' ' + ctx.getChild(1).getText() + ' ' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#MemberAccessExpr.
    def visitMemberAccessExpr(self, ctx:SolidityParser.MemberAccessExprContext):
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText() + self.visitIdentifier(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#PreCrementExpr.
    def visitPreCrementExpr(self, ctx:SolidityParser.PreCrementExprContext):
        return ctx.getChild(0).getText() + self.visit(ctx.getChild(1))


    # Visit a parse tree produced by SolidityParser#functionCallArguments.
    def visitFunctionCallArguments(self, ctx:SolidityParser.FunctionCallArgumentsContext):
        text = ctx.getChild(0).getText()
        for i in range(1, ctx.getChildCount() - 1):
            if hasattr(ctx.getChild(i), 'visit'):
                text += self.visit(ctx.getChild(i))
            else:
                text += ', '
        return text


    # Visit a parse tree produced by SolidityParser#tupleExpression.
    def visitTupleExpression(self, ctx:SolidityParser.TupleExpressionContext):
        text = '('
        for i in range(1, ctx.getChildCount() - 1):
            if hasattr(ctx.getChild(i), 'visit'):
                text += self.visit(ctx.getChild(i))
            else:
                text += ', '
        text += ')'
        return text


    # Visit a parse tree produced by SolidityParser#elementaryTypeNameExpression.
    def visitElementaryTypeNameExpression(self, ctx:SolidityParser.ElementaryTypeNameExpressionContext):
        return self.visitElementaryTypeName(ctx.getChild(0))


    # Visit a parse tree produced by SolidityParser#numberLiteral.
    def visitNumberLiteral(self, ctx:SolidityParser.NumberLiteralContext):
        return ctx.getText()


    # Visit a parse tree produced by SolidityParser#annotatedTypeName.
    # 변수의 타입
    def visitAnnotatedTypeName(self, ctx:SolidityParser.AnnotatedTypeNameContext):
        if ctx.getChildCount() == 1:
            return self.visitTypeName(ctx.getChild(0))
        else:
            return self.visitTypeName(ctx.getChild(0)) + '@' + self.visit(ctx.getChild(2))


    # Visit a parse tree produced by SolidityParser#identifier.
    def visitIdentifier(self, ctx:SolidityParser.IdentifierContext):
        return ctx.getText()
        # return self.visitChildren(ctx)

del SolidityParser